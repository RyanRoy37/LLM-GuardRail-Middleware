import re

# Example dictionary format for banned words by region (wrapped inside a list)
banned_words = [
    {
        "IND": [
            "fuck", "shit", "bitch", "asshole", "bastard",
            "madarchod", "bhenchod", "chutiya", "gandu", "randi",
            "saarasu", "poda", "kasu",
            "pichi", "gandu",
            "maderchod", "chutiya",
            "ricebag", "olahuuber", "puncturewala",
            "chapri", "neech", "ambedkarite",
            "terrorist", "commie", "dalit", "chamar",
            "sex", "porn", "pussy", "nude", "boobs", "penis", "vagina",
            "bomb", "kill", "murder", "drugs", "terror",
            "bakchod", "gandu", "chutiya",
            "modi", "rahul", "gandhi", "kejriwal", "yogi", "mamata", "amit shah", "priyanka", "sonia",
            "bjp", "congress", "aap", "shivsena", "cpi", "cpi(m)", "tdp", "trs", "dmk", "aiadmk",
            "hindu rashtra", "secularism", "communalism", "casteism", "dalit", "reservation", "saffronization",
            "leftist", "right wing", "liberal", "socialist", "communist", "nationalist", "populist", "maoist",
            "naxal", "terrorist", "extremist", "anti-national", "sedition",
            "jihad", "love jihad", "ghar wapsi", "beef ban", "citizenship amendment act", "caa", "nrc",
            "farmers protest", "kisan andolan", "bhim army", "khalistan", "separatist",
            "chinki", "madrasi", "bihari", "bangladeshi", "pakistani", "terrorist", "anti-social",
        ],
        "USA": [
            "fuck", "shit", "bitch", "asshole", "bastard", "damn", "crap", "dick", "piss", "cock",
            "nigger", "chink", "spic", "kike", "gook", "wetback", "cracker", "redneck",
            "sex", "porn", "xxx", "nude", "boobs", "penis", "vagina", "pussy", "dildo", "cum", "blowjob",
            "faggot", "dyke", "tranny", "retard", "cripple", "kafir", "infidel",
            "bomb", "kill", "murder", "drugs", "terror", "shoot", "gun",
            "slut", "whore", "cunt", "twat", "ass",
            "moron", "idiot", "dumbass", "loser",
            "trump", "biden", "obama", "hillary", "clinton", "republican", "democrat", "liberal", "conservative",
            "socialist", "communist", "capitalist", "fascist", "racist", "nationalist", "populist", "anarchist",
            "extremist", "terrorist", "immigrant", "refugee", "islamist", "islamophobia", "antisemitism",
            "racism", "sexism", "homophobia", "transphobia", "maga", "antifa", "qanon", "deep state", "fake news","twin towers", "9/11"
        ],
        "UK": [
            "fuck", "shit", "bitch", "arsehole", "wanker", "bollocks", "bugger", "prat", "tosser", "twat",
            "paki", "chink", "nigger", "coon", "spastic", "gypo", "tinker",
            "sex", "porn", "xxx", "nude", "boobs", "penis", "vagina", "pussy", "dildo", "cum", "blowjob",
            "faggot", "dyke", "tranny", "retard", "cripple", "infidel",
            "bomb", "kill", "murder", "drugs", "terror", "shoot", "gun",
            "slag", "git", "numpty", "muppet", "plonker", "bellend", "knobhead",
            "moron", "idiot", "dumbass", "loser",
            "brexit", "remain", "leave", "farage", "corbyn", "johnson", "labour", "tory", "conservative",
            "liberal", "socialist", "communist", "fascist", "racist", "nationalist", "populist", "anarchist",
            "extremist", "terrorist", "immigrant", "refugee", "islamist", "islamophobia", "antisemitism",
            "racism", "sexism", "homophobia", "transphobia"
        ]
    }
]

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search_in_text(self, text):
        text = text.lower()
        length = len(text)
        for i in range(length):
            node = self.root
            j = i
            current_word = ""
            while j < length and text[j] in node.children:
                node = node.children[text[j]]
                current_word += text[j]
                if node.is_end:
                    before = (i == 0) or (not text[i-1].isalnum())
                    after = (j == length - 1) or (not text[j+1].isalnum())
                    if before and after:
                        return current_word
                j += 1
        return None

# Flatten banned words dict inside list
banned_words_dict = banned_words[0]
flat_banned_words = set()
for region_words in banned_words_dict.values():
    for word in region_words:
        flat_banned_words.add(word.lower())

# Build trie
trie = Trie()
for word in flat_banned_words:
    trie.insert(word)

def contains_banned_word(sentence):
    return trie.search_in_text(sentence)

def mask_sensitive_info(sentence):
    # Email regex
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    sentence = re.sub(email_regex, '**', sentence)
    # International/US phone number regex
    phone_regex = r'(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}'
    sentence = re.sub(phone_regex, '**', sentence)
    # Indian phone number regex
    india_phone_regex = r'(?:\+91[\-\s]?|0)?[6-9]\d{9}\b'
    sentence = re.sub(india_phone_regex, '**', sentence)
    return sentence