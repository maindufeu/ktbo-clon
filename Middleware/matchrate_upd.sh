rm -rf Campaigns/facebook/*
rm -rf Campaigns/google/*
#rm -rf Campaigns/mp/*
#rm -rf Campaigns/othercampaigns/*
rm -rf Campaigns/sizmekco/*
rm -rf Campaigns/sizmekmx/*
rm -rf Campaigns/sizmekmi/*
rm -rf Campaigns/sizmekpr/*
#rm -rf Campaigns/twitter/*
#rm -rf Campaigns/youtube/*

chmod +x Campaigns/sftp_download.sh
./Campaigns/sftp_download.sh

python3 Campaigns/campaigns_unifier.py
python3 matchrate.py
