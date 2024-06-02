from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait_for_page_load(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))

test_mappings = {
    1: 'test_login_page_title',
    2: 'test_login_with_valid_credentials',
    3: 'test_login_with_invalid_credentials',
    4: 'test_loading_images',
    5: 'test_main_page_title',
    6: 'test_paragraph_quantity'
}

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
    
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # Retorno vacío si no hay coincidencias
            node = node.children[char]
        return self._collect_all_words(node, prefix)  # Usa el prefijo completo aquí

    def _collect_all_words(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            if child_node is not TrieNode:  # Asegura que child_node es una instancia
                words.extend(self._collect_all_words(child_node, prefix + char))
        return words