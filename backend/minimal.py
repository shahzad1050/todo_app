def handler(event, context):
    """
    A minimal Vercel Python function
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": '{"status": "ok", "message": "Minimal Python function works!"}'
    }