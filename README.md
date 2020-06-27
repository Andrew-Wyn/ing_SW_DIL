# ing\_SW\_DIL
document recognition

## Yolo
https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/

## OpenCV
https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/

## Idee
Single page web app -> Flask REST API -> Buisness logic (python module)

### Buisness logic (python module)
* Full-image recognition (YOLO? R-CNN?) -> abbiamo optato per mask_r-cnn per avere piu versatilita
* Ricerca oggetti rettangolari, correzione prospettica, riconoscimento locale

### todo: 
- fare training di un semplice modello single class document recognition -> prototipo (modello evolutivo)
