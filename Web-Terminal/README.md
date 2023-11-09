## Flask Web-Terminal Portfolio
> # Update 4: <br>
> <b>- New `migrations` for TODO list table.</b> <br>
> <b>- Added command `todo` / `cd todo`.</b> <br>
> <b>- Todo list is now connected to each user separately.</b> <br>
> <b>- Each task now has `[Due date]` field.</b> <br>
> <b>- `CRUD`: Each task can be marked/unmarked as "Done" or even removed completely.</b> <br>
> <b>- Restyled `[Date Selector]`.</b> <br>
<picture>
 <img src="https://cdn.discordapp.com/attachments/1051467735420370944/1172149323400749127/image.png?ex=655f4420&is=654ccf20&hm=6df13a044de5fd0ad27c0d42f040fb5cff81e035b7c5122e7551109c6b140beb&" alt="">
</picture>
<picture>
 <img src="https://cdn.discordapp.com/attachments/1051467735420370944/1172150045362094121/image.png?ex=655f44cc&is=654ccfcc&hm=17f98cb42b8f1f834df7eaf533c5da27f5a20bd8336d5872bfac9b43339b578d&" alt="">
</picture>

> # Update 3.1: <br>
> <b>- Added command `passwd`.</b> <br>
> <b>- `passwd` now checks for `session`, otherwise shows permission exception.</b> <br>
> <b>- `ChangePasswordForm` checks for equality for `pwd` & `confirm_pwd` through `EqualTo`</b> <br>
> <b>- New passwords are `hashed` as well.</b> <br>
> <b>- Fixed minor typos in different places.</b> <br>
> <b>- Fixed error colors displayed in `flash` messages.</b> <br>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1171328337076035594/image.png?ex=655c4785&is=6549d285&hm=67f1f6c8141644bd15334e7af20453201987a8b6a8887e65b28bd484df147078&=&width=1820&height=502" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1171328461860778144/image.png?ex=655c47a3&is=6549d2a3&hm=403c70232342d6ee5bc8d9bbf5315215b914247ce06b8223c7129aebdbae2c7f&=&width=1172&height=905" alt="">
</picture>

> # Update 3: <br>
> <b>- Commited `requirements.txt` file for easier setup.</b> <br>
> <b>- Comments are now displayed from newest to oldest.</b> <br>
> <b>- Added `feedback` command as well as it's hint in `help` and `ls`.</b> <br>
> <b>- Login page has been rewritten to use `flask_wtf` forms & `flash` messages.</b> <br>
> <b>- Users moved to `local database`.</b> <br>
> <b>- `app.secret_key` is now indeed secret.</b> <br>
> <b>- Users' passwords are now `hashed`.</b> <br>
> <b>- ... other changes that I simply can't remember.</b> <br>
<picture>
 <img src="https://cdn.discordapp.com/attachments/1051467735420370944/1171306044929101834/image.png?ex=655c32c2&is=6549bdc2&hm=c84bce8e4d2e779ed4e4d7da012876674b1e03f26ccb1e232790dc45ce2884cc&" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1171306114231582751/image.png?ex=655c32d3&is=6549bdd3&hm=9a3c895cebd8ebe9cecb06892dd4624abc1b74a10c3f03ec85423127bf060128&=&width=1416&height=905" alt="">
</picture>
<picture>
 <img src="https://cdn.discordapp.com/attachments/1051467735420370944/1171296780659462184/image.png?ex=655c2a22&is=6549b522&hm=66081ab8404636765c96020fd7ec0c15df9aa65c3f4cfce7a7b0be48a0ba7622&" alt="">
</picture>

> # Update 2: <br>
> <b>- Hosted on Arch Linux 6.5.9-arch2-1.</b> <br>
> <b>- Connection to database (`MariaDB`) along with migrations have been added.</b> <br>
> <b>- Feedback page implemented with use of `WTF forms`.</b> <br>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1169668812333916210/image.png?ex=65563df8&is=6543c8f8&hm=d8d9cc701371df524c2fdcd58e9e1e51cb53b9deb757eeebd5e265ea4c63165b&=" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1169672926950342676/image.png?ex=655641cd&is=6543cccd&hm=b2900d66c046d512f387759e3d10927a82d7010b7cbf734c517a251c34487ae2&=&width=802&height=847" alt="">
</picture>

<br>

> # Update 1: <br>
> <b>- User can be switched and allowed to save personal cookies.</b> <br>
> <b>- Directory is displayed instead of plain '~'.</b> <br>
> <b>- Restyled a bit more.</b> <br>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1165867887987269692/image.png?ex=65486a15&is=6535f515&hm=fe8c2a8582d807029bffefd2d755c16f52a751fafe598fb1475928cac8287b9e&=&width=1737&height=511" alt="">
</picture>

<br>

> # Release: <br>
> A website that I made using Flask/JS/Bootstrap/CSS/HTML Templates. <br>
> Provides terminal-like experience and info about my personality. <br>
> Supports multiple commands and route changes. <br>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1164368610123325523/image.png?ex=6542f5c5&is=653080c5&hm=a23ac1938422cce703d7205594af776f0623a15905facfbbc05e9a9904562a27&=&width=1102&height=798" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1164368772723904562/image.png?ex=6542f5ec&is=653080ec&hm=c8ba9d1124fa922fbb3c08df73f2b7021c87814df56cc1ad884eb7d7a58d0c08&=&width=1372&height=595" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1164368836921929810/image.png?ex=6542f5fb&is=653080fb&hm=211546b136b6ef674d941d88461d661776cf806e9b51c48682da4ead38cbe3aa&=&width=1372&height=780" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1164368974725787718/image.png?ex=6542f61c&is=6530811c&hm=a9e505de2f17b2e23bd54bd19bc11d4d7cb492510ccc768f98441950e780cd46&=&width=1144&height=798" alt="">
</picture>
<picture>
 <img src="https://media.discordapp.net/attachments/1051467735420370944/1164369063854735511/image.png?ex=6542f631&is=65308131&hm=08ec8144007cddf67a5d2eb2e1a0e712190374ec549b59a830ccee2029b09b6a&=&width=1372&height=782" alt="">
</picture>
