import unittest
from collections import Counter

from servers_skeleton import ListServer, Product, Client, MapServer, TooManyProductsFoundError, Server

server_types = (ListServer, MapServer)

class ServerTest(unittest.TestCase):
 
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))
    def  test_server_correctly_sorted_for_3_initial_letters(self):
        # sprawdza czy produkty są poprawnie posortowane
        # mają być w takiej samej kolejności jak szukasz czegoś
        # na allegro czyli od najtańszej
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1), Product('JDJ213', 1), Product('POP123', 100), Product("EZZ232", 3)]
        # Tworzy instancję serwera ListServer, który przyjmuje listę produktów.
        server = ListServer(products)
        # 3 to liczba początkowych liter w nazwie produktu
        entries = server.get_entries(3)
        # Sprawdź, czy wyniki (Counter) są zgodne z oczekiwanymi wynikami
        expected_entries = Counter([products[3], products[5], products[4]])
        actual_entries = Counter(entries)
        self.assertEqual(expected_entries, actual_entries)
    def test_if_exceeding_maximum_found_products_raises_exception(self):
        products = [Product('sS22', 13), Product('PG05', 12), Product('PS235', 35), Product('WV245', 69),
                    Product('Ck13', 15), Product('KN203', 86), Product('PL25', 2.5), Product('Rw100', 14)]
        for server_type in server_types :

            server = server_type(products)

            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2) 
        #Czy przekroczenie maksymalnej liczby znalezionych produktów powoduje rzucenie wyjątku?

class ClientTest(unittest.TestCase):
    #Czy funkcja obliczająca łączną cenę produktów zwraca poprawny wynik w przypadku rzucenia wyjątku 
    #oraz braku produktów pasujących do kryterium wyszukiwania?
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_get_total_price_handles_exception_case1(self):
        products = [Product('SS16', 41), Product('IO1223', 95), Product('POPP777', 135)]

        for server_type in server_types:
            with self.subTest(server_type=server_type):
                server = server_type(products)
                client = Client(server)
                total_price = client.get_total_price(10)
                self.assertIsNone(total_price)

    def test_get_total_price_handles_exception_case2(self):
        products = [Product('sS22', 13), Product('PG05', 12), Product('PS235', 35), Product('WV245', 69),
                    Product('Ck13', 15), Product('KN203', 86), Product('PL25', 2.5), Product('Rw100', 14)]

        for server_type in server_types:
            with self.subTest(server_type=server_type):
                server = server_type(products)
                client = Client(server)
                total_price = client.get_total_price(2)
                self.assertIsNone(total_price)


if __name__ == '__main__':
    unittest.main()
