// Swagger UI için JWT yetkilendirme
(function() {
    window.addEventListener('load', function() {
        // Swagger UI init'ten sonra çalış
        setTimeout(function() {
            const authBtn = document.querySelector('.auth-wrapper .authorize');
            const originalClick = authBtn.onclick;
            
            // Authorize butonuna özel davranış ekle
            authBtn.onclick = function() {
                originalClick.apply(this, arguments);
                
                // Authorize penceresinde Bearer token açıklaması ekle
                setTimeout(function() {
                    const bearerInput = document.querySelector('.auth-container input[type="text"]');
                    if (bearerInput) {
                        const helpText = document.createElement('div');
                        helpText.style.fontSize = '12px';
                        helpText.style.color = '#999';
                        helpText.style.margin = '5px 0';
                        helpText.innerHTML = 'Bearer token formatında giriş yapın: <strong>Bearer eyJhbGciOi...</strong>';
                        
                        bearerInput.parentNode.insertBefore(helpText, bearerInput.nextSibling);
                        
                        // "Bearer " öneki ekle
                        bearerInput.addEventListener('blur', function() {
                            if (this.value && !this.value.startsWith('Bearer ')) {
                                this.value = 'Bearer ' + this.value;
                            }
                        });
                    }
                }, 100);
            };
        }, 1000);
    });
})(); 