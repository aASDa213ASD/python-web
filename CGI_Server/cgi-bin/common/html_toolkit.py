import os


def refresh_page():
    script_name = os.environ.get("SCRIPT_NAME", "")
    http_host = os.environ.get("HTTP_HOST", "")
    server_port = os.environ.get("SERVER_PORT", "")

    # Construct the URL
    url = f"http://{http_host}:{server_port}{script_name}"

    # Print the HTTP response with the Location header
    print("Content-type: text/html")
    print(f"Location: {url}")
    print()

def get_head() -> str:
    return """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../assets/css/style.css">
    <title>CGI-BIN Server</title>

    <style>
        .main-content {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 80vh;
            margin: 0;
        }
    
        /* Style the form container */
        .form-container {
            max-width: 400px;
            min-height: 350px;
            padding: 25px;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        /* Style the header */
        header {
            padding: 10px;
        }

        /* Style the menu items */
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        nav a {
            color: white;
            text-decoration: none;
            
        }
    </style>

</head>
    """
