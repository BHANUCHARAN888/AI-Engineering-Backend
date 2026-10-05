request = {
    "method": "POST",
    "endpoint": "/predict",
    "body": {
        "hours_studied": 6,
        "attendance": 85
    }
}
def handle_request(request):
    if request["endpoint"] != "/predict":
        return {
            "status_code": 404,
            "body": {
                "error": "Endpoint not allowed"
            }
        }
    if request["method"] != "POST":
            return {
                "status_code": 405,
                "body": {
                    "error": "Method not allowed"
                }
            } 
    hours = request["body"]["hours_studied"]
    attendance = request["body"]["attendance"]
    if hours >= 5 and attendance >= 75:
         return {
              "status_code": 200,
              "body":{
                   "prediction": "Pass"
              }
         }
    else:
         return {
             "status_code": 200,
             "body": {
                  "prediction": "Fail"
              }
         }


         