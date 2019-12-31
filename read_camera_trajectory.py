import json,time
from unrealcv import client
from unrealcv.util import read_png,read_npy
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np
import os



home = os.getcwd()


camera='camera-trajectory-archinter.json'
camera_traj = json.load(open(camera))


data=os.path.join(home,camera[0:-5])
object_path = os.path.join(data,'object')
normal_path = os.path.join(data,'normal')
lit_path = os.path.join(data,'lit')
depth_path = os.path.join(data,'depth')
depth_image_path = os.path.join(data,'depth_image')
camera_pose_path = os.path.join(data,'camera_pose')
print(camera_pose_path)
if not os.path.exists(data):
        print('create file')
        os.mkdir(data)
        os.mkdir(object_path)
        os.mkdir(normal_path)
        os.mkdir(lit_path)
        os.mkdir(depth_path)
        os.mkdir(depth_image_path)
        os.mkdir(camera_pose_path)
  
client.connect()

print('wait 3s and start create picture')
time.sleep(3)
for i in range(len(camera_traj)):
    
    print('{x} {y} {z}'.format(x=camera_traj[i]['location'][0],y=camera_traj[i]['location'][1],z=camera_traj[i]['location'][2]))
    print('{x} {y} {z}'.format(x=camera_traj[i]['rotation'][0],y=camera_traj[i]['rotation'][1],z=camera_traj[i]['rotation'][2]))
    time.sleep(1)
    camera_str = str(camera_traj[i]['location'][0])+','+str(camera_traj[i]['location'][1])+','+str(camera_traj[i]['location'][2])+','+str(camera_traj[i]['rotation'][0])+','+str(camera_traj[i]['rotation'][1])+','+str(camera_traj[i]['rotation'][2])
    print(camera_str)#472.783,-204.083,95.24,357.459,40.746,0.0
    client.request('vset /camera/0/location {x} {y} {z}'.format(x=camera_traj[i]['location'][0],y=camera_traj[i]['location'][1],z=camera_traj[i]['location'][2]))
    client.request('vset /camera/0/rotation {x} {y} {z}'.format(x=camera_traj[i]['rotation'][0],y=camera_traj[i]['rotation'][1],z=camera_traj[i]['rotation'][2]))
    res_depth = client.request('vget /camera/0/depth npy')
    res_lit = client.request('vget /camera/0/lit png')
    res_object = client.request('vget /camera/0/object_mask png')
    res_normal = client.request('vget /camera/0/normal png')
    
    
    im_depth =read_npy(res_depth)
    #由於深度會有超過5000以上的值，圖會有白色的部分，因此把他指定為0，會轉為黑色
    im_depth[im_depth>5000]=0 
    im_lit = read_png(res_lit) 
    im_object = read_png(res_object)
    im_normal = read_png(res_normal)
   
    pil_img_depth = Image.fromarray(im_depth)
    pil_img_lit = Image.fromarray(im_lit)
    pil_img_object = Image.fromarray(im_object)
    pil_img_normal = Image.fromarray(im_normal)

    pil_img_depth = pil_img_depth.convert('RGB')    
#     pil_img_depth.save('./data_arch/depth_image/depth_image_{i}.png'.format(i=i))
    pil_img_depth.save(depth_image_path+'/depth_image_{i}.png'.format(i=i))
#     np.save('./data_arch/depth/depth_{i}'.format(i=i),im_depth)
    np.save(depth_path+'/dapth_{i}'.format(i=i),im_depth)
#     pil_img_lit.save('./data_arch/lit/lit_{i}.png'.format(i=i))
    pil_img_lit.save(lit_path+'/lit_{i}.png'.format(i=i))
#     pil_img_normal.save('./data_arch/normal/normal_{i}.png'.format(i=i))
    pil_img_normal.save(normal_path+'/normal_{i}.png'.format(i=i))
    
#     pil_img_object.save('./data_arch/object/object_{i}.png'.format(i=i))
    pil_img_object.save(object_path+'/object_{i}.png'.format(i=i))
    
    with open(camera_pose_path+'/camera_{i}.txt'.format(i=i),'w') as f:
        f.write(camera_str)
    
    