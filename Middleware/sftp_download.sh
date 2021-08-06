sshpass -p Eemaa9eiF4aeteigheiyu3Mae0piej sftp ktbo@sftp.adverity.com -22 << !
  cd uploads/test

  lcd Campaigns/facebook
  get facebook/*
  lcd ..
  lcd ..

  lcd Campaigns/sizmekpr
  get sizmekpr/*
  lcd ..
  lcd ..

  lcd Campaigns/sizmekmx
  get sizmekmx/*
  lcd ..
  lcd ..

  lcd Campaigns/sizmekmi
  get sizmekmi/*
  lcd ..
  lcd ..

  lcd Campaigns/sizmekco
  get sizmekco/*
  lcd ..
  lcd ..


  lcd Campaigns/google
  get google/*
  lcd ..
  lcd ..


  lcd Campaigns/youtube
  get youtube/*
  lcd ..
  lcd ..


#  lcd mp
#  get mp/*
#  lcd ..
#  rmdir mp
#  mkdir mp

#  lcd twitter
#  get twitter/*
#  lcd ..
#  rmdir twitter
#  mkdir twitter

#  lcd othercampaigns
#  get othercampaigns/*
#  lcd ..
#  rmdir othercampaigns
#  mkdir othercampaigns


  bye
!

aws s3 cp s3://othercampaigns/acumulado_other/pautas_locales_acumulado_other.xlsx Campaigns/othercampaigns/acumulado_other.xlsx
aws s3 cp s3://othercampaigns/acumulado_twitter/pautas_locales_acumulado_twitter.xlsx Campaigns/twitter/acumulado_twitter.xlsx
