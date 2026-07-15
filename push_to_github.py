import subprocess
import os

os.chdir(r'c:\TestBooking\Booking')

try:
    # Add all changes
    result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
    print('Add:', result.stdout, result.stderr)
    
    # Commit changes
    result = subprocess.run(['git', 'commit', '-m', 'Update: change background to dark and fix Styler crash'], capture_output=True, text=True)
    print('Commit:', result.stdout, result.stderr)
    
    # Push to GitHub
    result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
    print('Push:', result.stdout, result.stderr)
    
    if result.returncode == 0:
        print('\n✅ Successfully pushed to GitHub!')
    else:
        print('\n❌ Push failed. Check the output above.')
except Exception as e:
    print(f'Error: {e}')
