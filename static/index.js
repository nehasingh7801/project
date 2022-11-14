/*web cam access code with js*/
'use strict';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const errorMsgElement = document.getElementById('span#ErrorMsg');

const constraints = {
    /*no audio is required*/
    audio: false,
    video:{
        width: 640, height: 480
    }
};
//accessing the webcam
async function init(){
    try{
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    }catch(e){
        errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
}
//success
function handleSuccess(stream){
    window.stream = stream;
    video.srcObject = stream;
}
//load init
init();

//drawing the image
var context = canvas.getContext('2d');
snap.addEventListener('click', function(){
    context.drawImage(video, 0, 0, 640, 480);
    //Save image to flask server via ajax
    var dataURL = canvas.toDataURL();
    $.ajax({
    type: "POST",
    url: "/hook",
    data:{
        imageBase64: dataURL
    }
    }).done(function() {
    console.log('sent');
    });

    

});

