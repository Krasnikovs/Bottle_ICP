import os
import cloudComPy as cc
import math
import random
import numpy as np



path = '/home/goodchair/praksesafe/'
savePath = '/home/goodchair/praksesafe/result'

bottleDown = cc.loadPointCloud(os.path.join(path, 'cosmetic_down.ply'))
bottleUp = cc.loadPointCloud(os.path.join(path, 'cosmetic_up.ply'))
initBottleDown = cc.loadPointCloud(os.path.join(path, 'cosmetic_down.ply'))
initBottleUp = cc.loadPointCloud(os.path.join(path, 'cosmetic_up.ply'))

print('cloud name:')
print(bottleDown.getName())
print(bottleUp.getName())

print('Lower the score the better\n')

for count in range(1, 4, 1):
    alignBottle = bottleDown
    turnedBottle = initBottleDown

    degrees = random.uniform(0.0, 1.0)
    degrees = round(degrees, 2)
    
    turn = cc.ccGLMatrix()
    turn.initFromParameters(degrees*math.pi,(1., 1., 1.), (0., 0., 0.))
    alignBottle.applyRigidTransformation(turn)
    turnedBottle.applyRigidTransformation(turn)
    
    alignedBottle = cc.ICP(alignBottle, bottleUp, 1.5, 1200, 15000, True, cc.CONVERGENCE_TYPE.MAX_ITER_CONVERGENCE, False)
    score = alignedBottle.finalPointCount

    tranBottle = alignedBottle.transMat
    ICPbottle = alignedBottle.aligned
    ICPbottle.applyRigidTransformation(tranBottle)

    array44 = np.array(tranBottle.data())

    pricesDegrees = round(180*degrees)
    
    initBottleUp.setName('init_B')
    turnedBottle.setName('init_A')
    ICPbottle.setName('end_A')
    bottleUp.setName('end_B')

    initName = f"{count}_{pricesDegrees}_{score}_init.bin"
    endName = f"{count}_{pricesDegrees}_{score}_end.bin"
    arrayName = f"{count}_{pricesDegrees}_{score}_array.npy"

    cc.SaveEntities([turnedBottle, initBottleUp], os.path.join(savePath, initName))
    cc.SaveEntities([ICPbottle, bottleUp], os.path.join(savePath, endName))
    np.save(os.path.join(savePath, arrayName), array44)
    
    cycle = f"{count}. cycle complete"
    print(cycle)

