# Data for pytest
# This is where the tests variables are defined

URL = 'https://www.pythontutorial.net/' 
SECOND_URL = "https://justdvir.online/" # without www

# Example for a page with links inside that used in the testing
pages = [
    {
        'url': 'https://justdvir.online/',
        'links': [
            {'text': 'Link 1', 'url': 'https://www.linkedin.com/in/dvir-pashut-477992249/'},
            {'text': 'Link 2', 'url': 'https://github.com/dvir-pashut/portfolio-'},
            {'text': 'Link 3', 'url': 'https://github.com/dvir-pashut/portfolio-'},
            {'text': 'Link 4', 'url': 'https://persona-generator.today'},
            {'text': 'Link 4', 'url': 'https://persona-generator.today/'},
            {'text': 'Link 4', 'url': 'https://www.credly.com/badges/cd7f11f6-73b2-47dc-b5df-b737ef61a0fe/linked_in?t=rlwl2i'}
        ]
    },
]

