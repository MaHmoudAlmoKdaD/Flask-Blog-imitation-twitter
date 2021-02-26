from flaskblog import create_app

app = create_app()
# when we say (if __name__ == "__main__":) 
# اذا عم نشغل هالبرنامج من هالموديل _الفايل ءيلي نحنا فيو_ 
# اعمل 
# app.run(debug= True)
if __name__ == "__main__":
    app.run(debug=True)