import tqdm

from annoy import AnnoyIndex

class AnnoyUtils():
    def __init__(self):
        """ Generic class for annoy operations
    
        Attributes:
            None
        """
        self.ann_index = None
        self.image_list = []

        
    def set_image_list(self, image_list):
        print("setting image_list. length: {}".format(len(image_list)))
        self.image_list = image_list
    
    def prepare_annoy(self, vector_length=4096, metric='angular'):
        print("init annoy_index (vector_length:{}, metric:{})...".format(vector_length, metric))
        self.ann_index = AnnoyIndex(vector_length, metric)

    def build_index(self, n_trees=50):
        print("building index (n_trees:{})..".format(n_trees))
        self.ann_index.build(n_trees)

    def save_index(self, file_path='annoy.index'):
        print("saving index to file: {}..".format(file_path))
        self.ann_index.save(file_path)



    def query_similar_images_by_features(self, features, n_neighbors=51):
        """Function to retrivete similar features
            
            Args: 
                features: numpy.ndarray. feature vector
                n_neighbors: int. max number of neighbors
            
            Returns: 
                list. [image_ind, confidence]

        """
        search_results = self.ann_index.get_nns_by_vector(features, n_neighbors, include_distances=True)
        most_similars = []
        
        for j in range(len(search_results[0])):
            most_similars.append([search_results[0][j], search_results[1][j]]) #, self.image_list[search_results[0][j]]])
            
        return most_similars