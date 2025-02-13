from webScraping import WebScrap

def WebScrapingController(url):
    try:
        if url != "":
            return WebScrap(url)
        else:
            return {
                "message":"Invaild data !",
                "status":400
            }
    except Exception as e:
        return {
                "Error":str(e),
                "statusCode":500
            }