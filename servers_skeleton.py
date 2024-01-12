#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float) -> None:
        if not re.fullmatch('^[A-Za-z]+.*[0-9]+$', name):
            raise ValueError
        else:
            self.name = name
            self.price = price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self) -> int:
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, message="Too many products found") -> None:
        self.message = message
        super().__init__(self.message)


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania
class Server(ABC):
    n_max_returned_entries = 5

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        matches_list = []
        pattern = f'^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$'
        for product in self.get_products_list():
            if re.fullmatch(pattern, product.name):
                matches_list.append(product)
        if len(matches_list) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return matches_list

    @abstractmethod
    def get_products_list(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__products: List[Product] = products

    def get_products_list(self, n_letters: int = 1) -> List[Product]:
        return self.__products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__products: Dict[str, Product] = {}

        for product in products:
            self.__products[product.name] = product

    def get_products_list(self, n_letters: int = 1) -> List[Product]:
        v_list = list(self.__products.values())
        return v_list


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Server) -> None:
        self.server = server

    def calculate_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            if n_letters is None:
                products = self.server.get_entries()
            else:
                products = self.server.get_entries(n_letters)

            if len(products) == 0:
                return None

            total_price = sum(product.price for product in products)
            return total_price
        except TooManyProductsFoundError:
            return None

