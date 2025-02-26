let wallet = null;

async function connectWallet() {
    try {
        if (!window.solana || !window.solana.isPhantom) {
            alert('Please install Phantom wallet!');
            window.open('https://phantom.app/', '_blank');
            return;
        }

        const response = await window.solana.connect();
        wallet = response.publicKey.toString();
        updateWalletStatus();
        
        // Change button text
        document.getElementById('connect-wallet').textContent = 'Connected';
        document.getElementById('connect-wallet').style.background = 'var(--secondary-color)';
        
        // Show wallet status
        document.querySelector('.wallet-status').style.display = 'block';
    } catch (err) {
        console.error(err);
        alert('Failed to connect wallet: ' + err.message);
    }
}

async function updateWalletStatus() {
    if (!wallet) return;

    const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'));
    
    try {
        const balance = await connection.getBalance(new solanaWeb3.PublicKey(wallet));
        const solBalance = balance / solanaWeb3.LAMPORTS_PER_SOL;
        
        document.getElementById('wallet-address').textContent = `Address: ${wallet.slice(0, 4)}...${wallet.slice(-4)}`;
        document.getElementById('wallet-balance').textContent = `Balance: ${solBalance.toFixed(2)} SOL`;
    } catch (err) {
        console.error('Error fetching balance:', err);
    }
}

// Event Listeners
document.getElementById('connect-wallet').addEventListener('click', connectWallet);

// Animation for feature cards
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease-out';
    observer.observe(card);
});
