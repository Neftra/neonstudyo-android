# NeonStüdyo Akademi · Android

Bu depo, NeonStüdyo Akademi uygulamasını **GitHub Actions** ile otomatik olarak Android APK'sına çevirir. Bilgisayarına Android Studio kurman gerekmez.

## Test APK'sı almak
1. Depoya her yükleme yaptığında (veya **Actions › Android APK › Run workflow**) derleme kendiliğinden başlar (yaklaşık 5–8 dakika).
2. Bittiğinde **Actions** sekmesinde en üstteki yeşil çalışmaya tıkla.
3. Sayfanın altındaki **Artifacts** bölümünden `NeonStudyo-1.0.X` dosyasını indir, zip'i aç.
4. `NeonStudyo-test-1.0.X.apk` dosyasını telefona at ve kur (telefonda "bilinmeyen kaynaklardan yüklemeye izin ver" gerekir).

## Uygulamayı güncellemek
Sadece `www/index.html` dosyasını yenisiyle değiştir. Yükleme yapınca yeni APK otomatik üretilir; sürüm numarası her seferinde bir artar.

## Google Play için imzalı sürüm (sonra)
1. **Actions › Imza anahtari olustur (bir kez) › Run workflow**: bir şifre ve adını yaz.
2. Çıkan `imza-anahtari-GIZLI` dosyasını indir. İçindeki `neonstudyo-release.keystore` dosyasını ve şifreyi **güvenli bir yerde sakla**. Kaybedersen uygulamayı Play'de güncelleyemezsin.
3. **Settings › Secrets and variables › Actions › New repository secret** ile şunları ekle:
   - `KEYSTORE_BASE64`: `KEYSTORE_BASE64.txt` dosyasının içeriği
   - `KEYSTORE_PASSWORD`: şifren
   - `KEY_ALIAS`: `neonstudyo`
   - `KEY_PASSWORD`: şifren
4. Bundan sonraki her derlemede Google Play'e yüklenecek `.aab` dosyası da üretilir.

> Depoyu **Private** (gizli) tut.

Uygulama kimliği: `com.neonstudyo.akademi`
