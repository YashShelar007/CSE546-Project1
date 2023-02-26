const express = require('express');
const multer = require('multer');
const server = express();
const PORT = 3000;

const fs = require("fs");

const app = express();


const imagesUpload = multer({dest: __dirname + '/upload_images'})
const { sendMessage, receiveMessage, } = require("./sqsWebtier.js");
const { storeImage } = require("./storeImageinS3.js");

app.post("/", imagesUpload.single("myfile"), async(req, res) => {
   const s3Msg = await storeImage(req);
        //console.log(req.file.originalname);
    const sqsMsg = await sendMessage(req.file.originalname);

   // if(sqsMsg != undefined){
   //     await receiveMessage(req.file.originalname, res);
   // }

});

app.use(express.static('public'));


const hostname = "0.0.0.0";
app.listen(PORT, hostname, () => {
  console.log('Server listening on ${PORT}');
});
