from main import attach_names

# Skipped mocking API endpoints for purposes of simplicity
# Further tests could test invalid input data, many rows, or duplicates


def test_attach_names():
    movies_by_resource_id = {
        'https://example.org/films/1': {
            'id': 1,
            'name': 'Movie 1',
        },
        'https://example.org/films/2': {
            'id': 2,
            'name': 'Movie 2',
        },
        'https://example.org/films/3': {
            'id': 3,
            'name': 'Movie 3',
        }
    }

    persons = [{
        'name': 'John Doe',
        'films': [],
    }, {
        'name': 'Jane Doe',
        'films': ['https://example.org/films/3', 'https://example.org/films/1'],
    }]

    result = attach_names(movies_by_resource_id, persons)

    assert len(result) == 3

    assert result['https://example.org/films/1'].get('persons', []) == ['Jane Doe']
    assert len(result['https://example.org/films/2'].get('persons', [])) == 0
    assert result['https://example.org/films/3'].get('persons', []) == ['Jane Doe']
