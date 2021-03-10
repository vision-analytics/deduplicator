
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img

from tensorflow.keras.applications.vgg16 import preprocess_input


class FeatureExtractor:
    def __init__(self, img_size=224):
        """ Generic feature extractor class 
    
        Attributes:
            None
        """
        self.model = None
        self.img_size = img_size
        
        self.prepare_model()

    def prepare_model(self):
        print("preparing model...")
        # load vgg_model
        vgg_model = tf.keras.applications.vgg16.VGG16(weights='imagenet')

        # remove the last layers to extract features only
        self.model = tf.keras.models.Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc1").output) #fc2


    
    def preprocess_image(self, image_path):
        """Function to preprocess image for prediction
            
            Args: 
                image_path: str. image_path
            
            Returns: 
                numpy.ndarray. expanded_dims (1, x, x, 3) rgb

        """
        # load an image from file
        image = load_img(image_path, target_size=(self.img_size, self.img_size))

        # convert the image pixels to a numpy array
        image = img_to_array(image)

        # reshape data for the model
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

        # prepare the image for the VGG model
        image = preprocess_input(image)

        return image


    def extract_feature_for_single_image(self, image_path):
        """Function to extract features for single image
            
            Args: 
                image_path: str. image_path
            
            Returns: 
                numpy.ndarray. features (1, feature_length) 

        """
        
        if self.model is None:
            self.prepare_model()

        #preprocess image
        processed_image = self.preprocess_image(image_path)

        #extract features
        predictions = self.model.predict(processed_image)

        #print(predictions)
        return predictions

    def extract_feature_for_batch_images(self, image_paths):
        """Function to extract features for batch images
            
            Args: 
                image_paths: list. image_paths
            
            Returns: 
                numpy.ndarray. features (batch_size, feature_length) 

        """
        if self.model is None:
            self.prepare_model()

        processed_images=None

        #preprocess images (batch)
        for image_path in image_paths:        
            if processed_images is None:
                processed_images = self.preprocess_image(image_path)
            else:
                processed_images = np.concatenate((processed_images, self.preprocess_image(image_path)), axis=0)
                
        #extract features on batch
        predictions = self.model.predict_on_batch(processed_images)

        #print(predictions.shape)
        return predictions        