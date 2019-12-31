#### UnrealCV Project

https://unrealcv.org/

## Unreal is a Plugin with Unreal can create many type image


Step1: First you need to Download the Scene in Unreal create:

http://docs.unrealcv.org/en/master/reference/model_zoo.html


Step2: Install python3 package
- unrealcv
- numpy 
- Pillow
- python3-matplotlib

```
pip3 install -r requirement.txt
```

Step3: Open your Scene and record the trajectory

```
python3 create_camera_trajectory.py
```

Step4: Create image

```
python3 read_camera_trajectory.py
```