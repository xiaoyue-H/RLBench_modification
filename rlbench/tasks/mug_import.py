from typing import List, Tuple

from pyrep.const import PrimitiveShape
from pyrep.objects import Shape
import numpy as np

from rlbench.backend.spawn_boundary import SpawnBoundary
from rlbench.backend.task import Task
from rlbench.const import shapenet_mug

pi = 3.1415926

class MugImport(Task):

    def init_task(self) -> None:
        # TODO: This is called once when a task is initialised.
        self.drops = []
        self.boundary = Shape('boundary')

        x_values = np.arange(-0.4, 0.5, 0.1)
        y_values = np.arange(-0.4, 0.5, 0.1)
        self.coordinates = [[x, y, 0] for x in x_values for y in y_values]


    def init_episode(self, index: int) -> List[str]:
        # TODO: This is called at the start of each episode.
        self.drops = []

        self.mugs = self.my_sample(self.get_base(), 64, shapenet_mug)
        for i, mug in enumerate(self.mugs):

            mug.set_orientation([+pi / 2, 0, 0], relative_to=self.boundary)
            # [+pi / 2, 0, 0](y轴向上)
            # breakpoint()
            mug.set_position(self.coordinates[i], relative_to=self.boundary,
                                      reset_dynamics=False)
            self.drops.append(mug)

        # b = SpawnBoundary([Shape('boundary')])
        # b.sample(self.cup_source, min_distance=0.12)
        # b.sample(self.cup_target, min_distance=0.12)

        # b.sample(self.one_mug, min_distance=0.12)
        # [b.sample(d, min_distance=0.12) for d in self.distractors]

        # Make the waypoints always be the same orientation



        return ['']

    def variation_count(self) -> int:
        # TODO: The number of variations for this task.
        return 1

    def step(self) -> None:
        # Called during each sim step. Remove this if not using.
        pass

    def cleanup(self) -> None:
        # Called during at the end of each episode. Remove this if not using.
        for d in self.drops:
            d.remove()
        breakpoint()
        self.drops.clear()


    def base_rotation_bounds(self) -> Tuple[List[float], List[float]]:
        return [0, 0, 0], [0, 0, 0]

    def my_sample(self, target_base, num_samples, pathfile):
        created = []
        path_prefix = "/home/xiaoyue/shapenet/03797390/"
        path_suffix = "/models/model_normalized.obj"
        samples_path = np.random.choice(pathfile, num_samples, replace=False)
        for s in samples_path:
            ob = Shape.import_mesh(path_prefix + s + path_suffix,
                                   scaling_factor=0.1, ignore_up_vector=False)
            ob.set_renderable(True)
            ob.set_dynamic(False)
            ob.set_respondable(True)
            ob.set_model(True)
            ob.set_parent(target_base)
            created.append(ob)
        # print(len(created))

        return created