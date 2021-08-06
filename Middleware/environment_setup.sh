sudo yum update -y

sudo yum install openssh

wget http://sourceforge.net/projects/sshpass/files/latest/download -O sshpass.tar.gz
tar -xvf sshpass.tar.gz
cd sshpass-1.08
sudo yum groupinstall "Development Tools"
./configure
sudo make install

curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

pip3 install pandas
pip3 install datetime
pip3 install pydrive
pip3 install openpyxl

sudo yum install git-all -y
git --version
