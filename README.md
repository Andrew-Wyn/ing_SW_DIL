# ing\_SW\_DIL
document recognition

Initialize project with `pipenv install`

## Yolo
https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/

## Mask R-CNN
https://github.com/matterport/Mask_RCNN

## Annotator
http://www.robots.ox.ac.uk/~vgg/software/via/via.html

## OpenCV
https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/

## Sources
- https://medium.com/analytics-vidhya/instance-segmentation-using-mask-r-cnn-on-a-custom-dataset-78631845de2a

## Idee
Single page web app -> Flask REST API -> Buisness logic (python module)

### Buisness logic (python module)
* Full-image recognition (YOLO? R-CNN?) -> abbiamo optato per mask_r-cnn per avere piu versatilita
* Ricerca oggetti rettangolari, correzione prospettica, riconoscimento locale

### todo: 
- fare training di un semplice modello single class document recognition -> prototipo (modello evolutivo)

- ampliare il modello con altre classi, capire come rendere la cosa il piu trasparente possibile

- implementare ocr (capire quale delle opzioni discusse sono effettivamente piu logiche da applicare)

- sviluparre rest-full api per il management di un singolo frame

- sviluppare front end
