
# Termux Notification
termux-notification -t "Auto Absen" -c "$(python ~/skrip-malas/autoAbsenSimkuliah.py | tail -2)" --button2 'Coba Lagi' --button2-action 'bash ~/skrip-malas/termuxAPI-autoAbsenSimkuliah.sh';
