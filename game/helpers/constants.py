
class Constants:

    SLITHERIN_NAME = "Slitherin"
    ICON_PATH = "./assets/slitherin_icon.png"
    FONT = "Arial"
    MODEL_FEATURE_COUNT = 5 #[action_vector, left_neighbor_accessible, top_neighbor_accessible, right_point_accessible, self.get_angle_from_fruit()]
    MODEL_NAME = "model.tf"
    DQN_MODEL_NAME = "model.h5"
    CHECKPOINT_NAME = "model.ckpt"
    MODEL_DIRECTORY = "./tf_models/"
    NAVIGATION_BAR_HEIGHT = 30
    FPS = 10
    PIXEL_SIZE = 25
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 300
    FRAMES_TO_REMEMBER = 4
    SCREEN_DEPTH = 32
    ENV_HEIGHT = SCREEN_HEIGHT/PIXEL_SIZE
    ENV_WIDTH = SCREEN_WIDTH/PIXEL_SIZE
