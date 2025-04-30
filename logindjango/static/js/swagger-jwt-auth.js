// Swagger UI için JWT yetkilendirme özelleştirmesi
window.addEventListener('load', function() {
    // Swagger UI'nin yüklenmesi için biraz bekleyin
    setTimeout(function() {
        // Swagger dokümantasyonu sayfasında olduğumuzu kontrol et
        if (window.ui && document.querySelector('.swagger-ui')) {
            console.log("Swagger UI detected, applying customizations...");
            
            // Event listener ekleyerek authorize butonuna tıklamaları izle
            document.body.addEventListener('click', function(e) {
                // Authorize butonuna veya içindeki bir elemana tıklandı mı diye kontrol et
                if (e.target.classList.contains('authorize') || 
                    e.target.closest('.authorize')) {
                    
                    // Popup açıldığında müdahale etmek için biraz bekle
                    setTimeout(function() {
                        // API key input field'ını bul
                        const authInputs = document.querySelectorAll('.auth-container input[type="text"]');
                        
                        authInputs.forEach(function(input) {
                            // Bilgi metni ekle
                            const helpText = document.createElement('div');
                            helpText.style.color = '#999';
                            helpText.style.fontSize = '12px';
                            helpText.style.marginTop = '5px';
                            helpText.innerHTML = 'JWT token\'ı "Bearer" öneki ile girin. Örnek: <strong>Bearer eyJhbGciOi...</strong>';
                            
                            // Input'un bulunduğu parent'a bilgi metni ekle
                            if (input.parentNode && !input.parentNode.querySelector('.token-help-text')) {
                                input.parentNode.appendChild(helpText);
                                helpText.className = 'token-help-text';
                                
                                // Input'a event listener ekleyerek, "Bearer" öneki ekle
                                input.addEventListener('blur', function() {
                                    if (this.value && !this.value.trim().startsWith('Bearer ')) {
                                        this.value = 'Bearer ' + this.value.trim();
                                    }
                                });
                                
                                // Placeholder ekle
                                input.placeholder = 'Bearer token...';
                            }
                        });
                    }, 300);
                }
            }, true);
        }
    }, 1000);
}); 