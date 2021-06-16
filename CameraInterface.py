class ONICamera:
    """
    ---
    ONICamera
    ---
    ## Init:

    + depth_shape: frame shape supported by camera default. Defaults to (480, 640).

    + file_name: use file_name="xxxxx" to enable recorded file. Defaults to "".

    ## Methods:
    
    + get_a_depth_image: read a depth frame and output to ndarray(uint16)

    + view_depth: view depth image by matplotlib (support auto-draw color makes it easy to view)
    """    
    def __init__(self, depth_shape=(480, 640), file_name=""):
        """OPENNI Camera rtl test and device definition
        Args:
            depth_shape (tuple, optional): frame shape supported by camera default. Defaults to (480, 640).
            file_name (str, optional): use file_name="xxxxx" to enable recorded file. Defaults to "".
        """
        try:
            self.depth_shape = depth_shape
            from openni import openni2
            try:
                openni2.initialize()
                if file_name == "":
                    self.device = openni2.Device.open_any()
                else:
                    self.device = openni2.Device.open_file(bin(file_name))
            except Exception as e:
                print(repr(e))
                print("OPENNI2 Runtime Library not Found!!! Make sure your LD_LIBRARY_PATH or path-of-current containing runtime file.")
        except ImportError:
            print("Use `pip3 install openni` first")

    def get_a_depth_image(self):
        """read a depth frame and output to ndarray(uint16)
        Returns:
            np.ndarray: a uint16 array from depth frame
        """        
        try:
            import numpy as np
            ds = self.device.create_depth_stream()
            ds.start()
            _ = ds.read_frame()
            # read frame twice to make sure depth frame flush in memory, ARM arch special only ^_^.
            frame = ds.read_frame()
            ds.stop()
            return np.ndarray(self.depth_shape, dtype=np.uint16, buffer=frame.get_buffer_as_uint16())
        except ImportError:
            print("depth_image needs numpy supported.")
        except Exception as e:
            print("UNCACHED ERROR:", repr(e))

    def view_depth(self):
        """view depth image by matplotlib (support auto-draw color makes it easy to view)
        """        
        try:
            import matplotlib.pyplot as plt
            plt.imshow(self.get_a_depth_image)
            plt.title(f"ONICamera Depth Image ({self.depth_shape[1]}x{self.depth_shape[0]})")
            plt.show()
        except ImportError:
            print("view_depth needs matplotib supported.")
