# Türkçe Python Kod Editörü: PyNar

Bu proje kapsamında Python dili için açık kaynaklı tamamen Türkçe ara yüze sahip bir kodlama ortamı geliştirilmiştir. Bu sistem 3 katmanlı olarak tasarlanmıştır. Bu katmanlar; Kullanıcı ara yüzü Katmanı, Orta Katman ve Python yorumlayıcısı katmanlarıdır. Kullanıcı ara yüzü Katmanındaki bileşenler Python Kod Editörü ve Sohbet robotunun kullanıcı ara yüz birimleridir. Orta katmanda “Kod yapısal kontrol”, “Kod hata yöneticisi” ve “Zeki Etmen Alt Sistemi” bulunmaktadır.  “Kod yapısal kontrol modülü” kullanıcının kodundaki sözdizimsel (syntax) hatalarının tespitini yapmaktadır. Bu işlem kod çalıştırılmadan statik kod kontrol (static code checker) kütüphaneleriyle gerçekleştirilmektedir. “Kod hata yöneticisi”, kullanıcının yazdığı python kodunun python yorumlayıcı tarafından çalıştırılması sonucunda elde edilen hata bildirimlerini analiz etmektedir. Sohbet robotu (Chatbot Agent) ise bu çıkarımları kullanarak öğrencinin hatasının sebebini tespit etmekte ve buna bir çözüm önerecek makine öğrenmesi alt sistemi içermektedir. Kullanıcının hatasını çözebilecek olası en iyi çözüm tespit edilerek sohbet robotu aracılığıyla kullanıcıya aktarılmakta ve kullanıcı onay verirse kod içindeki hata düzeltilmektedir.

Önerdiğimiz bu sisteme "PyNar" adı verilmiştir. PyNar, kodlamaya yeni başlayanların kolay uyum sağlayabileceği ergonomiye sahip olacak şekilde kullanılabilirlik ilkeleri ışığında tasarlanmıştır. PyNar editörü tek başına bir masaüstü yazılım olarak kullanılabileceği gibi, yazılan kodları bulut ortamında depolama özelliğine de sahiptir. Bulut ortamında eğitici/öğretmen tarafından kullanıcıya atanan ödevleri alabilme ve öğrencilerin çözümlerini tekrar eğiticiye gönderebilme özelliklerine sahiptir. Ayrıca, her bir kullanıcının hata analizlerinin yapılabilmesine olanak sağlayarak öğrenmenin ne ölçüde gerçekleştiği raporlanabilmekte ve buna ek olarak çözümlerin intihal analizleri de gerçekleştirilebilmektedir.

Kodlama editörü tüm işletim sistemlerinde çalışabilir şekilde platform bağımsız masaüstü uygulama olarak geliştirilmiştir. Projenin tüm kodları, projenin tamamlanmasından sonra genel kullanıma açık bir kod deposuna yüklenmiş ve ülkemizdeki geliştiricilerin katkı verebilmesi için gerekli tüm teknik ve kullanıcı dokümantasyonları da oluşturulmuştur.  

Eğer Python bilginiz var ise aşağıda verilen "Kaynak Koddan Kurulum ve Çalıştırma" bölümündeki gibi kurup çalıştırabilirsiniz. Python'da yeni iseniz aşağıda indirme bağlantısı verilen Windows veya Linux için derlenmiş kurulum paketlerini indirip kurabilirsiniz. 

## Kaynak Koddan Kurulum ve Çalıştırma
### a) Windows 10 ve 11

Öncelikle bilgisayarınızda Python 3.8 veya yukarısı kurulu olmalıdır. Şu linkten indirebilirsiniz:

    https://www.python.org/downloads/

Eğer bilgisayarınızda git programı kurulu ise bu reponun yerel klonunu oluşturunuz. Git kullanmıyorsanız bu repoyu zip olarak indirip zip'i açınız. Bir komut satırı açınız ve Pynar_Beta-main klasörü içine giriniz.

Gerekli paketlerin kurulumu:

    pip install -r requirements.txt

![image](https://user-images.githubusercontent.com/854154/194746108-6d753b8b-2e2f-4626-a4ea-5d4e3844cd7b.png)

PyNar editör kod hatalarını kodu çalıştırmadan tespit edebilmek için açık kaynak kodlu [pyright](https://github.com/microsoft/pyright) adlı statik kod kontrol kütüphanesini kullanır. Pyright programının windows için derlenmiş sürümünü [şu linkten](https://www.pynar.org/releases/pyright/1.1.266/) indirip win.zip dosyasını herhangi bir yere açınız. Açtığınız yerdeki **pyright-win.exe** dosyasını ve **typeshed-fallback** klasörünü  **PyNar_Beta-main** içindeki **Bin** klasörü içine kopyalayınız.

Çalıştırmak için yine aynı klasördeyken aşağıdaki komut ile main.py dosyasını çalıştırınız.

    python main.py

![image](https://user-images.githubusercontent.com/854154/194746862-960109b6-0193-4304-8f8a-7a5026036206.png)


### b) Linux (Ubuntu, Pardus gibi Debian türevleri)

Pardus 21 sürümünü indirip kurunuz. Aşağıdaki paketleri kurunuz

    sudo apt-get update
    sudo apt-get install -y python3-pyqt5 python3-pip python3-unidecode python3-pyqt5.qtwebengine python3-pyqt5.qtsql python3-textdistance python3-pyqt5.qsci vulture python3-pycodestyle python3-natsort
    pip3 install emoji TurkishStemmer

Programı indirdiğiniz klasöre girerek

    python3 main.py

komutu ile çalıştırınız. Editör açıldıktan sonra ayarlar bölümünden Komutlar seçenek bölümünde "Pardus" seçiniz.

## Windows veya Linux için Derlenmiş Sürümler

Windows 10 ve 11 için Setup programı ve Linux için DEB paketleri şu linkten indirilebilir.

    https://www.pynar.org/releases/setup/

Paket indirildikten sonra windows için çift tıklayarak kurulum başlatılabilir. Kurulum programı bilgisayarınızda python yok ise otomatik kuracaktır.

    Not: Windows işletim sistenine bazı sürümlerde "SmartScreen" aktif ise "Windows bilgisayarınızı korudu" şeklinde bir mavi bildirim ekranı gelebilir. Bu durumda "Yine de Çalıştır" diyerek kuruluma devam edebilirsiniz. Pynar Editör kurulum programında bilgisayarınıza zarar vrecek hiçbirşey yoktur, Windows için maliyeti yüksek olduğundan sertifika almadığımız için bu uyarı gelmektedir.

Linux işletim sisteminde (Deb paket yöneticisi kullanan linuxlarda) kurulum için pynar.deb paketini indirdiğiniz klasörde aşağıdaki komut yazılmalıdır.

    sudo dpkg -i pynar.deb

Not: Windows kurulumu için yönetici yetkisi (Administrator) gerekli değildir, fakat Linux paketlerinin kurulumu için yönetici yetkisi (root) gereklidir.


## Özellikler ve Kullanım Kılavuzu

PyNar editörün tüm özellikleri ve kullanım kılavuzu aşağıdaki linkte yayınlanmaktadır.

    https://www.pynar.org/help


## PyNar Editör Ekran Görüntüsü:
![image](https://user-images.githubusercontent.com/30179132/112771996-18e20a00-9037-11eb-8832-7a828d10b3db.png)
