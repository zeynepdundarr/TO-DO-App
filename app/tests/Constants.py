class Constants:
        username = "Zeynep"
        password = username
        email = username+"@example.com"
        todo_id = 1
        a_todo_1 = {'category_label': 'self',
                'description': 'Sample todo is shown.',
                'id':1,
                'is_starred': False,
                'is_ticked': False,
                'owner_id': 1,
                'priority': '',
                'schedule': '',
                'status': 'pending',
                'title': 'Test Todo'}

        a_todo_2 = {'category_label': 'self',
                'description': 'Sample todo is shown.',
                'id':2,
                'is_starred': False,
                'is_ticked': False,
                'owner_id': 1,
                'priority': '',
                'schedule': '',
                'status': 'pending',
                'title': 'Test Todo'}
        
        a_todo_3 = {'category_label': 'self',
                'description': 'Sample todo is shown.',
                'id':3,
                'is_starred': False,
                'is_ticked': False,
                'owner_id': 1,
                'priority': '',
                'schedule': '',
                'status': 'pending',
                'title': 'Test Todo'}

        a_user_json = {"email": email, 
                        "username": username,
                        "password": password}

        user_form_data = {"grant_type": "password",
                        "username": username,
                        "password": password,
                        "scope": "",
                        "client_id": "",
                        "client_secret": ""}

        create_todo_header = {"accept": "application/json",
                                "authorization": f"Bearer {username}",
                                "content-type": "application/json"}

        authentication_header = {"accept": "application/json",
                                "Authorization": f"Bearer {username}"}