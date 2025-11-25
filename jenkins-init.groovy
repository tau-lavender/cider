import jenkins.model.*
import hudson.security.*

// Получаем экземпляр Jenkins
def instance = Jenkins.getInstance()

// Создаем режим безопасности с менеджером пользователей
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount("admin", "admin123")
instance.setSecurityRealm(hudsonRealm)

// Включаем авторизацию (например, полнофункциональную, без ограничений)
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
instance.setAuthorizationStrategy(strategy)

// Сохраняем настройки
instance.save()
