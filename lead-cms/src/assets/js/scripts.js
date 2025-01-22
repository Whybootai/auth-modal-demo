
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const modalOverlay = document.getElementById('modalOverlay');
    const notification = document.getElementById('notification');
    const listRange = document.getElementById('listRange');
    const modalText = document.getElementById('modalText');
    const freeBtn = document.getElementById('freeBtn');
    const bulkBtn = document.getElementById('bulkBtn');
    const pdfBtn = document.getElementById('pdfBtn');
    const csvBtn = document.getElementById('csvBtn');

    function showNotification() {
        modal.style.display = 'none';
        modalOverlay.style.display = 'none';
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }

    freeBtn.addEventListener('click', () => {
        modal.style.display = 'block';
        modalOverlay.style.display = 'block';
        modalText.textContent = 'Your free 50 leads are ready!';
        listRange.style.display = 'none';
    });

    bulkBtn.addEventListener('click', () => {
        modal.style.display = 'block';
        modalOverlay.style.display = 'block';
        modalText.textContent = 'Choose the number of local buyer leads needed:';
        listRange.style.display = 'block';
    });

    pdfBtn.addEventListener('click', showNotification);
    csvBtn.addEventListener('click', showNotification);

    modalOverlay.addEventListener('click', () => {
        modal.style.display = 'none';
        modalOverlay.style.display = 'none';
    });
});
