<h1>dreamhost-dns</h1>

<p>Uses the Dreamhost API to view and modify your DNS records. Very easy to use</p>
<p>
    Includes a single script that will update your domain's <em>A record</em> to your current <em>public IP address</em>.
    Running this on a cronjob would essentially give you DDNS for Dreamhost.
</p>

<h2><strong><u>First Use</u></strong></h2>

<h3><u>Installation</u></h3>

<p>Just download this github repo and remember the directory so you can create the config file in the next step.</p>

<h3><u>Setting Up Config File</u></h3>

<p>
    You will need an API token (get one at your <a href='https://panel.dreamhost.com/?tree=home.api'>Dreamhost API Key Web Panel</a>)
    with the three DNS functions -  <strong>dns-add_record</strong>, <strong>dns-list_records</strong>, <strong>dns-remove_record</strong>
</p>
<ul>
    <li>One you have your token, create a <strong><em>settings.ini</strong></em> file in this package's directory.</li>
    <li>In the settings.ini file place the following contents</li>
    <pre>[DREAMHOST]
token = {your-api-token}
domain = {your-domain-name}</pre>
    <li>Replace {your-api-token} with your API token</li>
    <li>Replace {your-domain-name} with the domain name that you want updated by the DDNS script</li>
    <li>Now you're all set to use the DDNS script or functions mentioned below</li>
</ul>

<h2><strong><u>DDNS Script</u></strong></h2>

<p>
    If you have the settings.ini file created and both the <samp>DREAMHOST token</samp> and <samp>DREAMHOST domain</samp> 
    settings set (instructions above), run the following  command to update that domain to your current public IP address.
    (Pulls IP address from <a href='https://api.ipify.org'>https://api.ipify.org</a>.)
</p>
<pre><code>python ddns.py</code></pre>
<p><strong>
    NOTE: It will not create the record (I may build this, it's like two lines of code I'd need to add) so you at least have to go to your Dreamhost DNS Records Web Panel and create the <em>A record</em> at least once. Instructions for that can be found <a href='https://help.dreamhost.com/hc/en-us/articles/360035516812#A_record'>here</a>.
</strong></p>
<p>
    This will not update the DNS record if it is already set to your current public IP address. This makes it so you can add 
    a cronjob and call this python script, essentially giving you DDNS for Dreamhost. Adding something like below to your crontab
    would check your current public IP address hourly, and update the DNS Record in Dreamhost for the domain you set if they don't match.
    Of course, you're free to do that on any schedule you'd like but your ISP shouldn't be changing your IP address that often.
</p>
<pre><code>@hourly /path/to/python /path/to/ddns.py</code></pre>
<p><strong>
    NOTE: Replace /path/to/python with that path to your machine's python.exe program
    and /path/to/ddns.py with the path to the ddns.py file downloaded from this repo.
</strong></p>

<h2><strong><u>Using Functions from this Package</u></strong></h2>

<p>If you import this package into your own script you will be able to use the following class and function.</p>

<h3><strong>def list_all_records()</strong></h3>

<p>A function that pulls all DNS records from the Dreamhost API and returns a list of DNSRecord objects.</p>

<h3><strong>class DNSRecord</strong></h3>

<p>A class that has a some functions making it easy to delete and update a DNS record using the Dreamhost API.</p>

<h4><em>&nbsp;&nbsp;&nbsp;&nbsp;def DNSRecord.remove_record()</em></h4>

<p>&nbsp;&nbsp;&nbsp;&nbsp;Deletes the record.</p>

<h4><em>&nbsp;&nbsp;&nbsp;&nbsp;def DNSRecord.update_record(value)</em></h4>

<p>&nbsp;&nbsp;&nbsp;&nbsp;Updates the record with the value that you give it.</p>

<h3><strong>def update_record_to_public()</strong></h3>

<p>This is all that runs when you runs ddns.py, so if you'd like to do that same thing in your own script then run this function.</p>