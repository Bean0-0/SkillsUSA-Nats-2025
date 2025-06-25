// Chrome Local Storage Downloader - Console Version
// Paste this code into Chrome's Developer Console (F12)

function downloadLocalStorageAsJSON() {
    // Get all local storage data
    const data = {};
    const stats = {
        itemCount: localStorage.length,
        totalSize: 0,
        domain: window.location.hostname,
        timestamp: new Date().toISOString()
    };

    // Collect all key-value pairs
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        const value = localStorage.getItem(key);
        data[key] = value;
        stats.totalSize += key.length + value.length;
    }

    const storageData = {
        metadata: stats,
        data: data
    };

    // Create and download JSON file
    const jsonString = JSON.stringify(storageData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `localstorage-${window.location.hostname}-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
    
    console.log(`✅ Downloaded local storage data!`);
    console.log(`📊 Items: ${stats.itemCount}, Size: ~${Math.round(stats.totalSize/1024)}KB`);
    console.log('📁 File saved as:', a.download);
    
    return storageData;
}

// Run the function
downloadLocalStorageAsJSON();
