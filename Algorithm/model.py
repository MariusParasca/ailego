class Model:

    def __init__(self, model=[]):
        self.model = model
        self.layers = []

    def is_stable(self):
        # is_stable = True
        unstable_layers_ids = []
        for layer_id, layer in enumerate(self.layers[:-1]):
            is_layer_stable = layer.is_stable_with_layer(self.layers[layer_id + 1])
            if is_layer_stable is not True:
                unstable_layers_ids.append((layer_id, layer_id + 1, is_layer_stable))
        if len(unstable_layers_ids) is 0:
            return True
        else:
            return unstable_layers_ids
