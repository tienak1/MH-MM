# Django Photo Sharing App

Source code for a SitePoint article demonstrating how to build a photo sharing app with login functionality using Python and Django.

## Features

- Django CRUD functionality
- User authentication 
    - Login
    - Logout
    - Sign-up
- Image Uploads
- Share image
- Hybrid Cipher
    - Encode/Decode image (Matrix cipher)
    - Encode/Decode matrix cipher key (RSA)
- Download decode image
- Reused code with Django Template Language
- Stylized pages with Bootstrap 5

## Requirements

* [Python](https://www.python.org/)

## SetUp

Clone the repository:
   - Original version: 
```bash
git clone https://github.com/sitepoint-editors/Django-photo-app
cd Django-photo-app/
```
   - My edited version:
```bash
git clone https://github.com/tienak1/MH-MM.git
cd config/
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it

```bash
source .venv/Scripts/activate
```

![Virtual environment activated](https://uploads.sitepoint.com/wp-content/uploads/2021/06/1622669492venv.png)

Install all the project dependencies with the `requirements.txt` with the following command.

```bash
pip install -r requirements.txt
```

```bash
cd config
```

Run the migrations:

```bash
python manage.py migrate
```

Run the project.

```bash
python manage.py runserver
```

Visit <http://localhost:8000/>.

![Main Page](https://uploads.sitepoint.com/wp-content/uploads/2021/05/1622404676list.png)

## Screenshots

![Dashboard](https://camo.githubusercontent.com/b91eb6691fa1cf9f611ba0b203f2e6f3e0c858de72a4374d5307c2005aff511a/68747470733a2f2f75706c6f6164732e73697465706f696e742e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032312f30352f313632323430343637366c6973742e706e67)

![Tag Dashboard](https://camo.githubusercontent.com/2c72474471d3074367f0dbbd5a60f652ec56f450186793639d40dc84d360a068/68747470733a2f2f75706c6f6164732e73697465706f696e742e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032312f30352f313632323430343637397461672d6c6973742e706e67)

![Detail page](https://camo.githubusercontent.com/9f9726e296539c66c5bab09984a5e3d9e8b9745fa0b0ac061f07e81f3ebd3e69/68747470733a2f2f75706c6f6164732e73697465706f696e742e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032312f30352f3136323234303534303566697273742d70686f746f2e706e67)

![Delete page](https://camo.githubusercontent.com/c694125655898730707b4cd0f04c7775401db3e3bea8d035d743b271bf78f2e3/68747470733a2f2f75706c6f6164732e73697465706f696e742e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032312f30352f3136323234313930323164656c6574652e706e67)

![Signup page](https://camo.githubusercontent.com/7e78e06bdf833096bc4231740d8a48384042cab423038e08aae7624d6aeeb4e6/68747470733a2f2f75706c6f6164732e73697465706f696e742e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032312f30352f313632323431393439337369676e75702e706e67)

## License

SitePoint's code archives and code examples are licensed under the MIT license.

Copyright © 2021 SitePoint

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
