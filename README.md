# VCM-Lip-Motion-Generator
## repo clone

```
git clone git@github.com:Yixing-Zhang/VCM-Lip-Motion-Generator.git --recursive 
cd VCM-Lip-Motion-Generator
```

## repo update
Do it when you want to update the repo to the lastest remote version. 
run the below command(make sure you are in the VCM-Lip-Motion-Generator folder currently)

```
git pull origin main
cd voca
git checkout master
git pull origin master
```
## model download 
Download the pretrained DeepSpeech model (v0.5.0) from [Mozilla/DeepSpeech](https://github.com/mozilla/DeepSpeech/releases/download/v0.5.0/deepspeech-0.5.0-models.tar.gz) (i.e. deepspeech-0.5.0-models.tar.gz).
And unzip it in folder ./voca/ds_graph.

Download the pretrained model from [pretrained model oneDrive sharing link](https://connecthkuhk-my.sharepoint.com/:u:/g/personal/ljt2021_connect_hku_hk/EfHFNnrI2N5GslR_JAGXgf8BSCka2EOIcnp_xdxbZQkhWQ?e=yuVKpV) (i.e. model.zip)
And unzip it in folder ./voca/model

## lip-sync model
for training and inferencing the lip-sync model, jump to the submodule [voca](https://github.com/Jeret-Ljt/voca/)

