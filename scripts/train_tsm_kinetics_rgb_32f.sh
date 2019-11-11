# You should get TSM_kinetics_RGB_resnet50_shift8_blockres_avg_segment32_e50
python main.py kinetics RGB \
     --arch resnet50 --num_segments 32 \
     --gd 20 --lr 0.01 --wd 1e-4 --lr_steps 20 40 --epochs 50 \
     --batch-size 64 -j 16 --dropout 0.5 --consensus_type=avg --eval-freq=1 \
     --shift --shift_div=8 --shift_place=blockres --npb