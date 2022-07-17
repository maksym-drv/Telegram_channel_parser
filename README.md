<h1 align="center">Telegram_channel_parser</h1>

<div>
<h2>:open_book: Description</h2>

<p>This program developed for Telegram messenger. By the help of this bot you can forward messages from one or more channel to another or anothers. The program's foundation is connections between sources and receivers. In the bot these connections called "nodes". Each node can contain infinity set of sources channel and infinity set of receive channel. After creation, the node have next setups:
</p>
<ul>
    <li>Adding new channels, both sources and receivers</li>
    <li>Deleting channels from the node</li>
    <li>Adding and deleting "hot words"</li>
    <li>Deleting node</li>
</ul>
<p>More about "Hot words". These are words which program search in messages from source channels. They have three option of setuping:</p>
<ol>
    <li>They can be cut from the message</li>
    <li>They can be replace in the message</li>
    <li>Ignore the message which contain these words</li>
</ol>
<p>
    Also, if you use hot words:
    <ul>
        <li>«https://» and «https://» which mean start of url</li>
        <li>«@» which mean start of Telegram username</li>
    </ul>
    program'll operate the full url or username, not just   theseindicated  text.
</p>
<p>For example, you indicate that <kbd>@</kbd> will replacing on the <kbd>friend</kbd>. If program get a message <kbd>Hello @mike, nice to meet!</kbd>, the message will look like <kbd>Hello friend, nice to meet!.</kbd></p>
<p>The program saves all messages from the source channels to make a message reply, so if you make the message reply in source, it will be make message reply on the same message in receive channel.</p>
<p>Finally, program have a 10 sec delay between sending Of during this time, the message is deleted in the source channel, it'll not send in receive channels.</p>
</div>
<div>
<h2>:floppy_disk: Installation</h2>
<p>First at all, we're cloning repository:</p>

```git
git clone https://github.com/maksymDrv/Telegram_channel_parser.git
```
<p>and and pulling docker image from my docker hub</p>

```docker
docker pull maksymdergachov/tg_channel_parser
```
<p>After that, you need to add your Telegram id to the file <kbd>/json/users.json</kbd>. This is necessary because the bot has its own security system. Users whose id isn't specified in the file cannot use the bot. The file with ID added should look like this:</p>

```json
[
    "123456789",
]
```
<p>In order to find out the ID of your account in the Telegram messenger, you can use one of the bots in the messenger itself. One of [them](https://t.me/userinfobot).</p>
<p>Next, you need to edit the environment files and add your database's and host's data. The first file is in the project folder <kbd>/env.dev</kbd> and the second file in <kbd>/parser/env.dev</kbd>. If you want to change default sending delay, you can change it here.</p>
<p>In <kbd>database_backup</kbd> folder you can find the backup of the database. You can use it for restoring your database.</p>
<p>As for Telegram API ID and Telegram API HASH, you can create them from this [link](https://my.telegram.org/auth).</p>
<p>Before starting you need to build your docker image by your code and data in environment file. Make it the command: </p>

```docker
docker-compose build
```
</div>
<div>
<h2>:rocket: Start</h2>
<p>For service starting you need to run Telegram bot and parser program. The bot in start by the command:</p>

```docker
docker-compose run -d
```
<p>Finally, start the parser by specifying your environment file:</p>

```docker
docker run -it --env-file parser/env.dev maksymdergachov/tg_channel_parser
```
<p>In creating new parser docker container you need to make Telegram authentication by the sending code.</p>
</div>