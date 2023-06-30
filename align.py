import os
import cloudComPy as cc
import random
import numpy as np
import pdb

path = '/home/goodchair/praksesafe/'
savePath = '/home/goodchair/praksesafe/Bottle_ICP/Example'

bottleDown = cc.loadPointCloud(os.path.join(path, 'mouthwash_down.ply'))
bottleUp = cc.loadPointCloud(os.path.join(path, 'mouthwash_up.ply'))
initBottleDown = bottleDown.cloneThis()
initBottleUp = bottleUp.cloneThis()

print('cloud name:')
print(bottleDown.getName())
print(bottleUp.getName())

for count in range(1, 6):
    alignBottle = bottleDown
    turnedBottle = initBottleDown

    rad = random.uniform(0.0, np.pi)
    
    turn = cc.ccGLMatrix()
    turn.initFromParameters(rad, (1., 1., 1.), (0., 0., 0.))
    alignBottle.applyRigidTransformation(turn)
    turnedBottle.applyRigidTransformation(turn)
    
    alignedBottle = cc.ICP(alignBottle, bottleUp, 1.e-100, 1200, 15000, False, cc.CONVERGENCE_TYPE.MAX_ITER_CONVERGENCE, False)
    score = "{:e}".format(alignedBottle.finalRMS)
    #pdb.set_trace()
    
    tranBottle = alignedBottle.transMat
    ICPbottle = alignedBottle.aligned
    ICPbottle.applyRigidTransformation(tranBottle)

    array44 = np.array(tranBottle.data())

    initBottleUp.setName('init_B')
    turnedBottle.setName('init_A')
    ICPbottle.setName('end_A')
    bottleUp.setName('end_B')

    initName = f"{count}_{score}_init.bin"
    endName = f"{count}_{score}_end.bin"
    arrayName = f"{count}_{score}_array.npy"

    cc.SaveEntities([turnedBottle, initBottleUp], os.path.join(savePath, initName))
    cc.SaveEntities([ICPbottle, bottleUp], os.path.join(savePath, endName))
    np.save(os.path.join(savePath, arrayName), array44)

    cycle = f"{count}.cycle complete"
    print(cycle)