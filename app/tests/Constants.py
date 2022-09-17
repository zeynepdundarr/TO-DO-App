class Constants:
        username_1 = "Zeynep"
        username_2 = "Irem"

        password = "Notsosecret"
        email_1 = username_1 + "@example.com"
        email_2 = username_2 + "@example.com"

        todo_id = 1
        modify_todo_id = 3
        a_todo_1 = {'category_label': 'self',
                'description': 'Sample todo is shown.',
                'id':1,
                'is_starred': False,
                'is_ticked': False,
                'owner_id': 1,
                'priority': '',
                'schedule': '',
                'status': 'done',
                'title': 'Test Todo'}

        a_todo_2 = {'category_label': 'self',
                'description': 'Sample todo is shown.',
                'id':2,
                'is_starred': False,
                'is_ticked': False,
                'owner_id': 1,
                'priority': '',
                'schedule': 'today',
                'status': 'done',
                'title': 'Test Todo'}
        
        a_todo_3 = {'category_label': 'home',
                'description': 'Sample todo is shown.',
                'id':3,
                'is_starred': False,
                'is_ticked': True,
                'owner_id': 1,
                'priority': '',
                'schedule': '',
                'status': 'pending',
                'title': 'Test Todo'}

        a_user_json = {"email": email_1, 
                        "username": username_1,
                        "password": password}
        
        a_user_json_same_email = {"email": email_1, 
                                "username": username_2,
                                "password": password}
        
        a_user_json_same_username = {"email": email_2, 
                                "username": username_1,
                                "password": password}

        a_user_form_data = {"grant_type": "password",
                        "username": username_1,
                        "password": password,
                        "scope": "",
                        "client_id": "",
                        "client_secret": ""}

        authentication_header = {"accept": "application/json",
                                "authorization": f"Bearer {username_1}",
                                "content-type": "application/json"}