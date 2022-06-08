
<h1>How to Deploying a Django Application to Elastic Beanstalk</h1>

<p><a href="https://aws.amazon.com/elasticbeanstalk/">AWS Elastic Beanstalk</a> (EB) is an easy-to-use service for deploying and scaling web applications. It connects multiple AWS services, like compute instances (<a href="https://aws.amazon.com/ec2/">EC2</a>), databases (<a href="https://aws.amazon.com/rds/">RDS</a>), load balancers (<a href="https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html">Application Load Balancer</a>), and file storage systems (<a href="https://aws.amazon.com/s3/">S3</a>), to name a few. EB allows you to quickly develop and deploy your web application without thinking about the underlying infrastructure. It <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html">supports</a> applications developed in Go, Java, .NET, Node.js, PHP, Python, and Ruby. EB also supports Docker if you need to configure your own software stack or deploy an application developed in a language (or version) that EB doesn't currently support.</p>




<p>There's no additional charge for AWS Elastic Beanstalk. You only pay for the resources that your application consumes.</p>
<p>To learn more about Elastic Beanstalk, check out <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html">What is AWS Elastic Beanstalk?</a> from the <a href="https://docs.aws.amazon.com/elastic-beanstalk/index.html">official AWS Elastic Beanstalk documentation</a>.</p>
<h3 id="elastic-beanstalk-concepts">Elastic Beanstalk Concepts</h3>
<p>Before diving into tutorial itself, let's look at a few key <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html">concepts</a> related to Elastic Beanstalk:</p>
<ol>
<li>An <strong><a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-application">application</a></strong> is a logical collection of Elastic Beanstalk components, including environments, versions, and environment configurations. An application can have multiple <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-version">versions</a>.</li>
<li>An <strong><a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-environment">environment</a></strong> is a collection of AWS resources running an application version.</li>
<li>A <strong><a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-platform">platform</a></strong> is a combination of an operating system, programming language runtime, web server, application server, and Elastic Beanstalk components.</li>
</ol>
<li>An <strong><a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-application">application</a></strong> is a logical collection of Elastic Beanstalk components, including environments, versions, and environment configurations. An application can have multiple <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-version">versions</a>.</li>
<li>An <strong><a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-environment">environment</a></strong> is a collection of AWS resources running an application version.</li>
<li>A <strong><a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html#concepts-platform">platform</a></strong> is a combination of an operating system, programming language runtime, web server, application server, and Elastic Beanstalk components.</li>
<p>These terms will be used throughout the tutorial.</p>
<h2 id="project-setup">Project Setup</h2>
<p>We'll be deploying a simple image hosting application called <a href="https://github.com/duplxey/django-images">django-images</a> in this tutorial.</p>
<p>Check your understanding by deploying your own application as you follow along with the tutorial.</p>
<p>First, grab the code from the <a href="https://github.com/duplxey/django-images">repository on GitHub</a>:</p>
<pre><span></span><code>$ git clone <a class="__cf_email__" data-cfemail="0d6a64794d6a647965786f236e6260" href="/cdn-cgi/l/email-protection">[email protected]</a>:duplxey/django-images.git
$ <span class="nb">cd</span> django-images
</code></pre>
<p>Create a new virtual environment and activate it:</p>
<pre><span></span><code>$ python3 -m venv venv <span class="o">&amp;&amp;</span> <span class="nb">source</span> venv/bin/activate
</code></pre>
<p>Install the requirements and migrate the database:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ pip install -r requirements.txt
<span class="o">(</span>venv<span class="o">)</span>$ python manage.py migrate
</code></pre>
<p>Run the server:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Open your favorite web browser and navigate to <a href="http://localhost:8000">http://localhost:8000</a>. Make sure everything works correctly by using the form on the right to upload an image. 

<h2 id="elastic-beanstalk-cli">Elastic Beanstalk CLI</h2>
<p>Be sure to <a href="https://portal.aws.amazon.com/billing/signup#/start">register</a> for an AWS account before continuing. By creating an account you might also be eligible for the <a href="https://aws.amazon.com/free/">AWS Free Tier</a>.</p>
<p>The <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html">Elastic Beanstalk command line interface</a> (EB CLI) allows you to perform a variety of operations to deploy and manage your Elastic Beanstalk applications and environments.</p>
<p>There are two ways of installing EB CLI:</p>
<ol>
<li>Via the <a href="https://github.com/aws/aws-elastic-beanstalk-cli-setup#2-quick-start">EB CLI installer</a></li>
<li>With <a href="https://pypi.org/project/awsebcli/">pip (awsebcli)</a></li>
</ol>
<li>Via the <a href="https://github.com/aws/aws-elastic-beanstalk-cli-setup#2-quick-start">EB CLI installer</a></li>
<li>With <a href="https://pypi.org/project/awsebcli/">pip (awsebcli)</a></li>
<p>It's recommended to install the EB CLI globally (outside any specific virtual environment) using the installer (first option) to avoid possible dependency conflicts. Refer to <a href="https://github.com/aws/aws-elastic-beanstalk-cli-setup#51-for-the-experienced-python-developer-whats-the-advantage-of-this-mode-of-installation-instead-of-regular-pip-inside-a-virtualenv">this explanation</a> for more details.</p>
<p>After you've installed the EB CLI, you can check the version by running:</p>
<pre><span></span><code>$ eb --version

EB CLI <span class="m">3</span>.20.3 <span class="o">(</span>Python <span class="m">3</span>.10.<span class="o">)</span>
</code></pre>
<p>If the command doesn't work, you may need to add the EB CLI to <code>$PATH</code>.</p>
<p>A list of EB CLI commands and their descriptions can be found in the <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cmd-commands.html">EB CLI command reference</a>.</p>
<h2 id="initialize-elastic-beanstalk">Initialize Elastic Beanstalk</h2>
<p>Once we have the EB CLI running we can start interacting with Elastic Beanstalk. Let's initialize a new project along with an EB Environment.</p>
<h3 id="init">Init</h3>
<p>Within the project root ("django-images"), run:</p>
<pre><span></span><code>$ eb init
</code></pre>
<p>You'll be prompted with a number of questions.</p>
<h4 id="default-region">Default Region</h4>
<p>The AWS region of your Elastic Beanstalk environment (and resources). If you're not familiar with the different AWS regions, check out <a href="https://aws.amazon.com/about-aws/global-infrastructure/regions_az/">AWS Regions and Availability Zones</a>. Generally, you should pick the region that's closest to your customers. Keep in mind that resource prices vary from region to region.</p>
<h4 id="application-name">Application Name</h4>
<p>This is the name of your Elastic Beanstalk application. I recommend just pressing enter and going with the default: "django-images".</p>
<h4 id="platform-and-platform-branch">Platform and Platform Branch</h4>
<p>The EB CLI will detect that you're using a Python environment. After that, it'll give you different Python versions and Amazon Linux versions you can work with. Pick "Python 3.8 running on 64bit Amazon Linux 2".</p>
<h4 id="codecommit">CodeCommit</h4>
<p><a href="https://aws.amazon.com/codecommit/">CodeCommit</a> is a secure, highly scalable, managed source control service that hosts private Git repositories. We won't be using it since we're already using GitHub for source control. So say "no".</p>
<h4 id="ssh">SSH</h4>
<p>To connect to the EC2 instances later we need to set up SSH. Say "yes" when prompted.</p>
<h4 id="keypair">Keypair</h4>
<p>To connect to EC2 instances, we'll need an RSA keypair. Go ahead and generate one, which will be added to your "~/.ssh" folder.</p>
<p>After you answer all the questions, you'll notice a hidden directory inside your project root named ".elasticbeanstalk". The directory should contain a <em>config.yml</em> file, with all the data you've just provided.</p>
<pre><span></span><code>.elasticbeanstalk
└── config.yml
</code></pre>
<p>The file should contain something similar to:</p>
<pre><span></span><code><span class="nt">branch-defaults</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">master</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="nt">environment</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="w">    </span><span class="nt">group_suffix</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="nt">global</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">application_name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">django-images</span><span class="w"></span>
<span class="w">  </span><span class="nt">branch</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="w">  </span><span class="nt">default_ec2_keyname</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">aws-eb</span><span class="w"></span>
<span class="w">  </span><span class="nt">default_platform</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Python 3.8 running on 64bit Amazon Linux 2</span><span class="w"></span>
<span class="w">  </span><span class="nt">default_region</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">us-west-2</span><span class="w"></span>
<span class="w">  </span><span class="nt">include_git_submodules</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">true</span><span class="w"></span>
<span class="w">  </span><span class="nt">instance_profile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="w">  </span><span class="nt">platform_name</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="w">  </span><span class="nt">platform_version</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="w">  </span><span class="nt">profile</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">eb-cli</span><span class="w"></span>
<span class="w">  </span><span class="nt">repository</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">null</span><span class="w"></span>
<span class="w">  </span><span class="nt">sc</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">git</span><span class="w"></span>
<span class="w">  </span><span class="nt">workspace_type</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">Application</span><span class="w"></span>
</code></pre>
<h3 id="create">Create</h3>
<p>Next, let's create the Elastic Beanstalk environment and deploy the application:</p>
<pre><span></span><code>$ eb create
</code></pre>
<p>Again, you'll be prompted with a few questions.</p>
<h4 id="environment-name">Environment Name</h4>
<p>This represents the name of the EB environment. I'd recommend sticking with the default: "django-images-env".</p>
<p>It's considered good practice to add <code>└-env</code> or <code>└-dev</code> suffix to your environments so you can easily differentiate EB apps from environments.</p>
<h4 id="dns-cname-prefix">DNS CNAME Prefix</h4>
<p>Your web application will be accessible at <code>%cname%.%region%.elasticbeanstalk.com</code>. Again, use the default.</p>
<h4 id="load-balancer">Load balancer</h4>
<p>A load balancer distributes traffic amongst your environment's instances. Select "application".</p>
<p>If you want to learn about the different load balancer types, review <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.elb.html">Load balancer for your Elastic Beanstalk Environment</a>.</p>
<h4 id="spot-fleet-requests">Spot Fleet Requests</h4>
<p><a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html">Spot Fleet</a> requests allow you to launch instances on-demand based on your criteria. We won't be using them in this tutorial, so say "no".</p>
<p>--</p>
<p>With that, the environment will be spun up:</p>
<ol>
<li>Your code will be zipped up and uploaded to a new S3 Bucket.</li>
<li>After that, the various AWS resources will be created, like the load balancer, security and auto-scaling groups, and EC2 instances.</li>
</ol>
<li>Your code will be zipped up and uploaded to a new S3 Bucket.</li>
<li>After that, the various AWS resources will be created, like the load balancer, security and auto-scaling groups, and EC2 instances.</li>
<p>A new application will be deployed as well.</p>
<p>This will take about three minutes so feel free to grab a cup of coffee.</p>
<p>After the deployment is done, the EB CLI will modify <em>.elasticbeanstalk/config.yml</em>.</p>
<p>Your project structure should now look like this:</p>
<pre><span></span><code><span class="p">|</span>-- .elasticbeanstalk
<span class="p">|</span>   └-- config.yml
<span class="p">|</span>-- .gitignore
<span class="p">|</span>-- README.md
<span class="p">|</span>-- core
<span class="p">|</span>   <span class="p">|</span>-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- asgi.py
<span class="p">|</span>   <span class="p">|</span>-- settings.py
<span class="p">|</span>   <span class="p">|</span>-- urls.py
<span class="p">|</span>   └-- wsgi.py
<span class="p">|</span>-- db.sqlite3
<span class="p">|</span>-- images
<span class="p">|</span>   <span class="p">|</span>-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- admin.py
<span class="p">|</span>   <span class="p">|</span>-- apps.py
<span class="p">|</span>   <span class="p">|</span>-- forms.py
<span class="p">|</span>   <span class="p">|</span>-- migrations
<span class="p">|</span>   <span class="p">|</span>   <span class="p">|</span>-- 0001_initial.py
<span class="p">|</span>   <span class="p">|</span>   └-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- models.py
<span class="p">|</span>   <span class="p">|</span>-- tables.py
<span class="p">|</span>   <span class="p">|</span>-- templates
<span class="p">|</span>   <span class="p">|</span>   └-- images
<span class="p">|</span>   <span class="p">|</span>       └-- index.html
<span class="p">|</span>   <span class="p">|</span>-- tests.py
<span class="p">|</span>   <span class="p">|</span>-- urls.py
<span class="p">|</span>   └-- views.py
<span class="p">|</span>-- manage.py
└-- requirements.txt
</code></pre>
<h3 id="status">Status</h3>
<p>Once you've deployed your app you can check its status by running:</p>
<pre><span></span><code>$ eb status

Environment details <span class="k">for</span>: django-images-env
Application name: django-images
Region: us-west-2
Deployed Version: app-93ec-220218_095635133296
Environment ID: e-z7dmesipvc
Platform: arn:aws:elasticbeanstalk:us-west-2::platform/Python <span class="m">3</span>.8 running on 64bit Amazon Linux <span class="m">2</span>/3.3.10
Tier: WebServer-Standard-1.0
CNAME: django-images-env.us-west-2.elasticbeanstalk.com
Updated: <span class="m">2022</span>-02-18 <span class="m">16</span>:00:24.954000+00:00
Status: Ready
Health: Red
</code></pre>
<p>You can see that our environment's current health is <code>Red</code>, which means that something went wrong. Don't worry about this just yet, we'll fix it in the next steps.</p>
<p>You can also see that AWS assigned us a CNAME which is our EB environment's domain name. We can access the web application by opening a browser and navigating to the CNAME.</p>
<h3 id="open">Open</h3>
<pre><span></span><code>$ eb open
</code></pre>
<p>This command will open your default browser and navigate to the CNAME domain. You'll see <code>502 Bad Gateway</code>, which we'll fix here shortly</p>
<h3 id="console">Console</h3>
<pre><span></span><code>$ eb console
</code></pre>
<p>This command will open the Elastic Beanstalk console in your default browser.</p>


<p>Again, you can see that the health of the environment is "Severe", which we'll fix in the next step.</p>
<h2 id="configure-an-environment">Configure an Environment</h2>
<p>In the previous step, we tried accessing our application and it returned <code>502 Bad Gateway</code>. There are a few reasons behind it:</p>
<ol>
<li>Python needs <code>PYTHONPATH</code> in order to find modules in our application.</li>
<li>By default, Elastic Beanstalk attempts to launch the WSGI application from <em>application.py</em>, which doesn't exist.</li>
<li>Django needs <code>DJANGO_SETTINGS_MODULE</code> to know which settings to use.</li>
</ol>
<li>Python needs <code>PYTHONPATH</code> in order to find modules in our application.</li>
<li>By default, Elastic Beanstalk attempts to launch the WSGI application from <em>application.py</em>, which doesn't exist.</li>
<li>Django needs <code>DJANGO_SETTINGS_MODULE</code> to know which settings to use.</li>
<p>By default Elastic Beanstalk serves Python applications with <a href="https://gunicorn.org/">Gunicorn</a>. EB automatically installs Gunicorn in the deployment process, hence we do not have to add it to <em>requirements.txt</em>. If you want to swap Gunicorn with something else, take a look at <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-configuration-procfile.html">Configuring the WSGI server with a Procfile</a>.</p>
<p>Let's fix these errors.</p>
<p>Create a new folder in the project root called ".ebextensions". Within the newly created folder create a file named <em>01_django.config</em>:</p>
<pre><span></span><code><span class="c1"># .ebextensions/01_django.config</span><span class="w"></span>

<span class="n">option_settings</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">application</span><span class="p">:</span><span class="n">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">DJANGO_SETTINGS_MODULE</span><span class="p">:</span><span class="w"> </span><span class="s2">"core.settings"</span><span class="w"></span>
<span class="w">    </span><span class="n">PYTHONPATH</span><span class="p">:</span><span class="w"> </span><span class="s2">"/var/app/current:$PYTHONPATH"</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">container</span><span class="p">:</span><span class="n">python</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">WSGIPath</span><span class="p">:</span><span class="w"> </span><span class="s2">"core.wsgi:application"</span><span class="w"></span>
</code></pre>
<p>Notes:</p>
<ol>
<li>We set the <code>PYTHONPATH</code> to the Python path on our EC2 instance (<a href="https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH">docs</a>).</li>
<li>We pointed <code>DJANGO_SETTINGS_MODULE</code> to our Django settings (<a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-specific.html#command-options-python">docs</a>).</li>
<li>We changed the <code>WSGIPath</code> to our WSGI application (<a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-specific.html#command-options-python">docs</a>).</li>
</ol>
<li>We set the <code>PYTHONPATH</code> to the Python path on our EC2 instance (<a href="https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH">docs</a>).</li>
<li>We pointed <code>DJANGO_SETTINGS_MODULE</code> to our Django settings (<a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-specific.html#command-options-python">docs</a>).</li>
<li>We changed the <code>WSGIPath</code> to our WSGI application (<a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-specific.html#command-options-python">docs</a>).</li>
<p>How do EB <em>.config</em> files work?</p>
<ol>
<li>You can have as many as you want.</li>
<li>They are loaded in the following order: 01_x, 02_x, 03_x, etc.</li>
<li>You do not have to memorize these settings; you can list all your environmental settings by running <code>eb config</code>.</li>
</ol>
<li>You can have as many as you want.</li>
<li>They are loaded in the following order: 01_x, 02_x, 03_x, etc.</li>
<li>You do not have to memorize these settings; you can list all your environmental settings by running <code>eb config</code>.</li>
<p>If you want to learn more about advanced environment customization check out <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html">Advanced environment customization with configuration files</a>.</p>
<p>At this point your project structure should look like this:</p>
<pre><span></span><code><span class="p">|</span>-- .ebextensions
<span class="p">|</span>   └-- 01_django.config
<span class="p">|</span>-- .elasticbeanstalk
<span class="p">|</span>   └-- config.yml
<span class="p">|</span>-- .gitignore
<span class="p">|</span>-- README.md
<span class="p">|</span>-- core
<span class="p">|</span>   <span class="p">|</span>-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- asgi.py
<span class="p">|</span>   <span class="p">|</span>-- settings.py
<span class="p">|</span>   <span class="p">|</span>-- urls.py
<span class="p">|</span>   └-- wsgi.py
<span class="p">|</span>-- db.sqlite3
<span class="p">|</span>-- images
<span class="p">|</span>   <span class="p">|</span>-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- admin.py
<span class="p">|</span>   <span class="p">|</span>-- apps.py
<span class="p">|</span>   <span class="p">|</span>-- forms.py
<span class="p">|</span>   <span class="p">|</span>-- migrations
<span class="p">|</span>   <span class="p">|</span>   <span class="p">|</span>-- 0001_initial.py
<span class="p">|</span>   <span class="p">|</span>   └-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- models.py
<span class="p">|</span>   <span class="p">|</span>-- tables.py
<span class="p">|</span>   <span class="p">|</span>-- templates
<span class="p">|</span>   <span class="p">|</span>   └-- images
<span class="p">|</span>   <span class="p">|</span>       └-- index.html
<span class="p">|</span>   <span class="p">|</span>-- tests.py
<span class="p">|</span>   <span class="p">|</span>-- urls.py
<span class="p">|</span>   └-- views.py
<span class="p">|</span>-- manage.py
└-- requirements.txt
</code></pre>
<p>Another thing we have to do before redeploying is to add our CNAME to the <code>ALLOWED_HOSTS</code> in <em>core/settings.py</em>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">ALLOWED_HOSTS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">'xyz.elasticbeanstalk.com'</span><span class="p">,</span>  <span class="c1"># make sure to replace it with your own EB CNAME</span>
<span class="p">]</span>
</code></pre>
<p>Alternatively, for testing, you could just use a wildcard: <code>ALLOWED_HOSTS = ['*']</code>. Just don't forget to change that after you're done testing!</p>
<p>Commit the changes to git and deploy:</p>
<pre><span></span><code>$ git add .
$ git commit -m <span class="s2">"updates for eb"</span>

$ eb deploy
</code></pre>
<p>You'll notice that Elastic Beanstalk won't detect the changes if you don't commit. That's because EB integrates with git and only detects the committed (changed) files.</p>
<p>After the deployment is done, run <code>eb open</code> to see if everything worked</p>
<p>Ouch. We fixed the previous error, but there's a new one now:</p>
<pre><span></span><code>NotSupportedError at /
<span class="nv">deterministic</span><span class="o">=</span>True requires SQLite <span class="m">3</span>.8.3 or higher
</code></pre>
<p>Don't worry. It's just an issue with SQLite, which shouldn't be used in production anyways. We'll swap it with Postgres here shortly.</p>
<h2 id="configure-rds">Configure RDS</h2>
<p>Django uses a <a href="https://www.sqlite.org/index.html">SQLite</a> database by <a href="https://docs.djangoproject.com/en/4.0/ref/databases/#sqlite-notes">default</a>. While this is perfect for development, you'll typically want to move to a more robust database, like Postgres or MySQL, for production. What's more, the current EB platform doesn't work well with SQLite, because of a version dependency conflict. Because of these two things we'll swap out SQlite for <a href="https://www.postgresql.org/">Postgres</a>.</p>
<h3 id="local-postgres">Local Postgres</h3>
<p>First, let's get Postgres running locally. You can either download it from <a href="https://www.postgresql.org/download/">PostgreSQL Downloads</a> or spin up a Docker container:</p>
<pre><span></span><code>$ docker run --name django-images-postgres -p <span class="m">5432</span>:5432 <span class="se">\</span>
-e <span class="nv">POSTGRES_USER</span><span class="o">=</span>django-images -e <span class="nv">POSTGRES_PASSWORD</span><span class="o">=</span>complexpassword123 <span class="se">\</span>
-e <span class="nv">POSTGRES_DB</span><span class="o">=</span>django-images -d postgres
</code></pre>
<p>Check if the container is running:</p>
<pre><span></span><code>$ docker ps -f <span class="nv">name</span><span class="o">=</span>django-images-postgres

CONTAINER ID   IMAGE      COMMAND                  CREATED              STATUS              PORTS                    NAMES
c05621dac852   postgres   <span class="s2">"docker-entrypoint.s…"</span>   About a minute ago   Up About a minute   <span class="m">0</span>.0.0.0:5432-&gt;5432/tcp   django-images-postgres
</code></pre>
<p>Now, let's try connecting to it with our Django app. Inside <em>core/settings.py</em>, change the <code>DATABASE</code> config to the following:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">DATABASES</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'ENGINE'</span><span class="p">:</span> <span class="s1">'django.db.backends.postgresql_psycopg2'</span><span class="p">,</span>
<span class="s1">'NAME'</span><span class="p">:</span> <span class="s1">'django-images'</span><span class="p">,</span>
<span class="s1">'USER'</span><span class="p">:</span> <span class="s1">'django-images'</span><span class="p">,</span>
<span class="s1">'PASSWORD'</span><span class="p">:</span> <span class="s1">'complexpassword123'</span><span class="p">,</span>
<span class="s1">'HOST'</span><span class="p">:</span> <span class="s1">'localhost'</span><span class="p">,</span>
<span class="s1">'PORT'</span><span class="p">:</span> <span class="s1">'5432'</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">}</span>
</code></pre>
<p>Next, install <a href="https://pypi.org/project/psycopg2-binary/">psycopg2-binary</a>, which is required for Postgres:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ pip install psycopg2-binary<span class="o">==</span><span class="m">2</span>.9.3
</code></pre>
<p>Add it to <em>requirements.txt</em>:</p>
<pre><span></span><code>Django==4.0.2
Pillow==9.0.1
django-tables2==2.4.1
django-crispy-forms==1.14.0
psycopg2-binary==2.9.3
</code></pre>
<p>Create and apply the migrations:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py makemigrations
<span class="o">(</span>venv<span class="o">)</span>$ python manage.py migrate
</code></pre>
<p>Run the server:</p>
<pre><span></span><code><span class="o">(</span>venv<span class="o">)</span>$ python manage.py runserver
</code></pre>
<p>Make sure you can still upload an image at <a href="http://localhost:8000">http://localhost:8000</a>.</p>
<p>If you get a <code>DisallowedHost</code> error, add <code>localhost</code> and <code>127.0.0.1</code> to <code>ALLOWED_HOSTS</code> inside <em>core/settings.py</em>.</p>
<h3 id="aws-rds-postgres">AWS RDS Postgres</h3>
<p>To set up Postgres for production, start by running the following command to open the AWS console:</p>
<pre><span></span><code>$ eb console
</code></pre>
<p>Click "Configuration" on the left side bar, scroll down to "Database", and then click "Edit".</p>
<p>Create a DB with the following settings and click on "Apply":</p>
<li>Engine: postgres</li>
<li>Engine version: 12.9 (older Postgres version since db.t2.micro is not available with 13.1+)</li>
<li>Instance class: db.t2.micro</li>
<li>Storage: 5 GB (should be more than enough)</li>
<li>Username: pick a username</li>
<li>Password: pick a strong password</li>

<p>After the environmental update is done, EB will automatically pass the following DB credentials to our Django app:</p>
<pre><span></span><code>RDS_DB_NAME
RDS_USERNAME
RDS_PASSWORD
RDS_HOSTNAME
RDS_PORT
</code></pre>
<p>We can now use these variables in <em>core/settings.py</em> to set up the <code>DATABASE</code>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="k">if</span> <span class="s1">'RDS_DB_NAME'</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">:</span>
<span class="n">DATABASES</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'ENGINE'</span><span class="p">:</span> <span class="s1">'django.db.backends.postgresql_psycopg2'</span><span class="p">,</span>
<span class="s1">'NAME'</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'RDS_DB_NAME'</span><span class="p">],</span>
<span class="s1">'USER'</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'RDS_USERNAME'</span><span class="p">],</span>
<span class="s1">'PASSWORD'</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'RDS_PASSWORD'</span><span class="p">],</span>
<span class="s1">'HOST'</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'RDS_HOSTNAME'</span><span class="p">],</span>
<span class="s1">'PORT'</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'RDS_PORT'</span><span class="p">],</span>
<span class="p">}</span>
<span class="p">}</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">DATABASES</span> <span class="o">=</span> <span class="p">{</span>
<span class="s1">'default'</span><span class="p">:</span> <span class="p">{</span>
<span class="s1">'ENGINE'</span><span class="p">:</span> <span class="s1">'django.db.backends.postgresql_psycopg2'</span><span class="p">,</span>
<span class="s1">'NAME'</span><span class="p">:</span> <span class="s1">'django-images'</span><span class="p">,</span>
<span class="s1">'USER'</span><span class="p">:</span> <span class="s1">'django-images'</span><span class="p">,</span>
<span class="s1">'PASSWORD'</span><span class="p">:</span> <span class="s1">'complexpassword123'</span><span class="p">,</span>
<span class="s1">'HOST'</span><span class="p">:</span> <span class="s1">'localhost'</span><span class="p">,</span>
<span class="s1">'PORT'</span><span class="p">:</span> <span class="s1">'5432'</span><span class="p">,</span>
<span class="p">}</span>
<span class="p">}</span>
</code></pre>
<p>Don't forget to import the <code>os</code> package at the top of <em>core/settings.py</em>:</p>
<pre><span></span><code><span class="kn">import</span> <span class="nn">os</span>
</code></pre>
<p>Next, we have to tell Elastic Beanstalk to run <code>makemigrations</code> and <code>migrate</code> when a new application version gets deployed. We can do that by editing the <em>.ebextensions/01_django.config</em> file. Add the following to the bottom of the file:</p>
<pre><span></span><code><span class="c1"># .ebextensions/01_django.config</span><span class="w"></span>

<span class="n">container_commands</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="mi">01</span><span class="n">_makemigrations</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py makemigrations --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">02</span><span class="n">_migrate</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py migrate --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
</code></pre>
<p>The EB environment will now execute the above commands every time we deploy a new application version. We used <code>leader_only</code>, so only the first EC2 instance executes them (in case our EB environment runs multiple EC2 instances).</p>
<p>Elastic Beanstalk configs support two different command sections, <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html#linux-commands">commands</a> and <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html#linux-container-commands">container_commands</a>. The main difference between them is when they are run in the deployment process:</p>
<ol>
<li><code>commands</code> run before the application and web server are set up and the application version file is extracted.</li>
<li><code>container_commands</code> run after the application and web server have been set up and the application version archive has been extracted, but before the application version is deployed (before the files are moved from the staging folder to their final location).</li>
</ol>
<li><code>commands</code> run before the application and web server are set up and the application version file is extracted.</li>
<li><code>container_commands</code> run after the application and web server have been set up and the application version archive has been extracted, but before the application version is deployed (before the files are moved from the staging folder to their final location).</li>
<p>Let's also add a command to create a superuser. We can use Django's intuitive <a href="https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/">custom command framework</a> to add a new command. Within the "images" app create the following files and folders:</p>
<pre><span></span><code>└-- images
└-- management
<span class="p">|</span>-- __init__.py
└-- commands
<span class="p">|</span>-- __init__.py
└-- createsu.py
</code></pre>
<p><em>createsu.py</em>:</p>
<pre><span></span><code><span class="c1"># images/management/commands/createsu.py</span>

<span class="kn">from</span> <span class="nn">django.contrib.auth.models</span> <span class="kn">import</span> <span class="n">User</span>
<span class="kn">from</span> <span class="nn">django.core.management.base</span> <span class="kn">import</span> <span class="n">BaseCommand</span>


<span class="k">class</span> <span class="nc">Command</span><span class="p">(</span><span class="n">BaseCommand</span><span class="p">):</span>
<span class="n">help</span> <span class="o">=</span> <span class="s1">'Creates a superuser.'</span>

<span class="k">def</span> <span class="nf">handle</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">options</span><span class="p">):</span>
<span class="k">if</span> <span class="ow">not</span> <span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">filter</span><span class="p">(</span><span class="n">username</span><span class="o">=</span><span class="s1">'admin'</span><span class="p">)</span><span class="o">.</span><span class="n">exists</span><span class="p">():</span>
<span class="n">User</span><span class="o">.</span><span class="n">objects</span><span class="o">.</span><span class="n">create_superuser</span><span class="p">(</span>
<span class="n">username</span><span class="o">=</span><span class="s1">'admin'</span><span class="p">,</span>
<span class="n">password</span><span class="o">=</span><span class="s1">'complexpassword123'</span>
<span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s1">'Superuser has been created.'</span><span class="p">)</span>
</code></pre>
<p>Next, add the third container command to <em>.ebextensions/01_django.config</em>:</p>
<pre><span></span><code><span class="c1"># .ebextensions/01_django.config</span><span class="w"></span>

<span class="n">container_commands</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="mi">01</span><span class="n">_makemigrations</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py makemigrations --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">02</span><span class="n">_migrate</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py migrate --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="c1"># ------------------------------------- new -------------------------------------</span><span class="w"></span>
<span class="w">  </span><span class="mi">03</span><span class="n">_superuser</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py createsu"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="c1"># --------------------------------- end of new  ---------------------------------</span><span class="w"></span>
</code></pre>
<p>An alternative to creating a <code>createsu</code> command is to SSH into one of the EC2 instances and run Django's default <code>createsuperuser</code> command.</p>
<p>Commit the changes to git and deploy:</p>
<pre><span></span><code>$ git add .
$ git commit -m <span class="s2">"updates for eb"</span>

$ eb deploy
</code></pre>
<p>Wait for the deployment to finish. Once done, run <code>eb open</code> to open your app in a new browser tab. Your app should now work. Make sure you can upload an image.</p>
<h2 id="s3-for-file-storage">S3 for File Storage</h2>
<p>Check out the deployed version of your admin dashboard. The static files aren't being served correctly. Further, we don't want static or media files stored locally on an EC2 instance since EB applications should be as stateless, which makes it much easier to <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html#concepts.concepts.design.scalability">scale</a> your applications out to multiple EC2 instances.</p>
<p>While AWS provides a number of <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html#concepts.concepts.design.storage">persistent storage</a> services, <a href="https://aws.amazon.com/s3/">S3</a> is arguably the most popular and easiest to work with.</p>
<p>To configure S3, we'll need to:</p>
<ol>
<li>Create an S3 Bucket</li>
<li>Create an IAM group and user for S3 Bucket management</li>
<li>Set Elastic Beanstalk S3 environment variables</li>
<li>Configure Django static and media settings</li>
</ol>
<li>Create an S3 Bucket</li>
<li>Create an IAM group and user for S3 Bucket management</li>
<li>Set Elastic Beanstalk S3 environment variables</li>
<li>Configure Django static and media settings</li>
<h3 id="create-an-s3-bucket">Create an S3 Bucket</h3>
<p>To start, let's create a new S3 Bucket. Navigate to the <a href="https://s3.console.aws.amazon.com/s3/home">AWS S3 Console</a> and click on "Create Bucket". Give the Bucket a unique name and set the AWS region. Use the default config for everything else. Press "Create".</p>
<h3 id="iam-group-and-user">IAM Group and User</h3>
<p>Navigate to the <a href="https://console.aws.amazon.com/iamv2/home">IAM Console</a>. On the left side of the screen, select "User groups". Create a new group with the "AmazonS3FullAccess" permission:</p>

<p>Then, create a new user with "Programmatic access" and assign that group to the user.</p>

<p>AWS will generate authentication credentials for you. Download the provided <em>.csv</em> file. We'll need to pass them to our Elastic Beanstalk environment in the next step.</p>
<h3 id="set-eb-environment-variables">Set EB Environment Variables</h3>
<p>Next, we need to set the following environmental variables:</p>
<pre><span></span><code><span class="n">AWS_ACCESS_KEY_ID</span><span class="w">                </span><span class="o">-</span><span class="w"> </span><span class="n">your</span><span class="w"> </span><span class="n">ACCESS_KEY_ID</span><span class="w"></span>
<span class="n">AWS_SECRET_ACCESS_KEY</span><span class="w">            </span><span class="o">-</span><span class="w"> </span><span class="n">your</span><span class="w"> </span><span class="n">SECRET_ACCESS_KEY</span><span class="w"></span>
<span class="n">AWS_S3_REGION_NAME</span><span class="w">               </span><span class="o">-</span><span class="w"> </span><span class="n">your</span><span class="w"> </span><span class="n">selected</span><span class="w"> </span><span class="n">S3</span><span class="w"> </span><span class="n">region</span><span class="w"></span>
<span class="n">AWS_STORAGE_BUCKET_NAME</span><span class="w">          </span><span class="o">-</span><span class="w"> </span><span class="n">your</span><span class="w"> </span><span class="n">bucket</span><span class="w"> </span><span class="n">name</span><span class="w"></span>
</code></pre>
<p>Navigate to your Elastic Beanstalk console. Click "Configuration". Then, within the "Software" category, click "Edit" and scroll down to the "Environment properties" section. Add the four variables.</p>

<p>After you've added all the variables click "Apply".</p>
<h3 id="configure-django-static-and-media-settings">Configure Django Static and Media Settings</h3>
<p>Next, in order for Django to communicate with our S3 Bucket, we need to install the <a href="https://django-storages.readthedocs.io/en/latest/">django-storages</a> and <a href="https://aws.amazon.com/sdk-for-python/">boto3</a> packages.</p>
<p>Add them to the <em>requirements.txt</em> file:</p>
<pre><span></span><code>Django==4.0.2
Pillow==9.0.1
django-tables2==2.4.1
django-crispy-forms==1.14.0
psycopg2-binary==2.9.3
boto3==1.21.3
django-storages==1.12.3
</code></pre>
<p>Next, add the newly installed app to <code>INSTALLED_APPS</code> in <em>core/settings.py</em>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="c1"># ...</span>
<span class="s1">'storages'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p>Configure django-storages to use the environmental variables passed by Elastic Beanstalk:</p>
<pre><span></span><code><span class="k">if</span> <span class="s1">'AWS_STORAGE_BUCKET_NAME'</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">:</span>
<span class="n">STATICFILES_STORAGE</span> <span class="o">=</span> <span class="s1">'storages.backends.s3boto3.S3Boto3Storage'</span>
<span class="n">DEFAULT_FILE_STORAGE</span> <span class="o">=</span> <span class="s1">'storages.backends.s3boto3.S3Boto3Storage'</span>

<span class="n">AWS_STORAGE_BUCKET_NAME</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'AWS_STORAGE_BUCKET_NAME'</span><span class="p">]</span>
<span class="n">AWS_S3_REGION_NAME</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'AWS_S3_REGION_NAME'</span><span class="p">]</span>

<span class="n">AWS_S3_ACCESS_KEY_ID</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'AWS_ACCESS_KEY_ID'</span><span class="p">]</span>
<span class="n">AWS_S3_SECRET_ACCESS_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'AWS_SECRET_ACCESS_KEY'</span><span class="p">]</span>
</code></pre>
<p>Lastly, we need to run the <code>collectstatic</code> command after deployment is complete, so add the following to the bottom of <em>01_django.config</em>:</p>
<pre><span></span><code><span class="c1"># .ebextensions/01_django.config</span><span class="w"></span>
<span class="c1"># ...</span><span class="w"></span>

<span class="n">container_commands</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="c1"># ...</span><span class="w"></span>
<span class="w">  </span><span class="mi">04</span><span class="n">_collectstatic</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py collectstatic --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
</code></pre>
<p>The full file should now look like this:</p>
<pre><span></span><code><span class="c1"># .ebextensions/01_django.config</span><span class="w"></span>

<span class="n">option_settings</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">application</span><span class="p">:</span><span class="n">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">DJANGO_SETTINGS_MODULE</span><span class="p">:</span><span class="w"> </span><span class="s2">"core.settings"</span><span class="w"></span>
<span class="w">    </span><span class="n">PYTHONPATH</span><span class="p">:</span><span class="w"> </span><span class="s2">"/var/app/current:$PYTHONPATH"</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">container</span><span class="p">:</span><span class="n">python</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">WSGIPath</span><span class="p">:</span><span class="w"> </span><span class="s2">"core.wsgi:application"</span><span class="w"></span>

<span class="n">container_commands</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="mi">01</span><span class="n">_makemigrations</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py makemigrations --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">02</span><span class="n">_migrate</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py migrate --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">03</span><span class="n">_superuser</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py createsu"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">04</span><span class="n">_collectstatic</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py collectstatic --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
</code></pre>
<p>Commit the changes to git and deploy:</p>
<pre><span></span><code>$ git add .
$ git commit -m <span class="s2">"updates for eb"</span>

$ eb deploy
</code></pre>
<p>Confirm that the static and media files are now stored on S3.</p>
<p>If you get a <code>Signature mismatch</code> error, you might want to add the following setting to <em>core/settings.py</em>: <code>AWS_S3_ADDRESSING_STYLE = "virtual"</code>. For more details, refer to <a href="https://github.com/jschneier/django-storages/issues/782">this GitHub issue</a>.</p>
<p>To learn more about static and media file storage on AWS S3, take a look at the <a href="/blog/storing-django-static-and-media-files-on-amazon-s3/">Storing Django Static and Media Files on Amazon S3</a> article.</p>
<h2 id="https-with-certificate-manager">HTTPS with Certificate Manager</h2>
<p>This part of the tutorial requires that you have a domain name.</p>
<p>Need a cheap domain to practice with? Several domain registrars have specials on '.xyz' domains. Alternatively, you can create a free domain at <a href="https://www.freenom.com/">Freenom</a>. If you don't own a domain name, but would still like to use HTTPS you can <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-ssl.html">create and sign with an X509 certificate</a>.</p>
<p>To serve your application via HTTPS, we'll need to:</p>
<ol>
<li>Request and validate an SSL/TLS certificate</li>
<li>Point your domain name to your EB CNAME</li>
<li>Modify the load balancer to serve HTTPS</li>
<li>Modify your application settings</li>
</ol>
<li>Request and validate an SSL/TLS certificate</li>
<li>Point your domain name to your EB CNAME</li>
<li>Modify the load balancer to serve HTTPS</li>
<li>Modify your application settings</li>
<h3 id="request-and-validate-an-ssltls-certificate">Request and Validate an SSL/TLS Certificate</h3>
<p>Navigate to the <a href="https://console.aws.amazon.com/acm/">AWS Certificate Manager console</a>. Click "Request a certificate". Set the certificate type to "Public" and click "Next". Enter your <a href="https://docs.aws.amazon.com/acm/latest/userguide/setup-domain.html">fully qualified domain name</a> into the form input, set the "Validation method" to "DNS validation", and click "Request".</p>

<p>You'll then be redirected to a page where you can see all your certificates. The certificate that you just created should have a status of "Pending validation".</p>
<p>For AWS to issue a certificate, you first have to prove that you're the owner of the domain. In the table, click on the certificate to view the "Certificate details". Take note of the "CNAME name" and "CNAME value". To validate the ownership of the domain, you'll need to create a CNAME Record" in your domain's DNS settings. Use the "CNAME name" and "CNAME value" for this. Once done, it will take a few minutes for Amazon to pick up the domain changes and issue the certificate. The status should change from "Pending validation" to "Issued".</p>
<h3 id="point-the-domain-name-to-the-eb-cname">Point the Domain Name to the EB CNAME</h3>
<p>Next, you need to point your domain (or subdomain) to your EB environment CNAME. Back in your domain's DNS settings, add another CNAME record with the value being your EB CNAME -- e.g., <code>django-images-dev.us-west-2.elasticbeanstalk.com</code>.</p>
<p>Wait a few minutes for your DNS to refresh before testing things out from the <code>http://</code> flavor of your domain name in your browser.</p>
<h3 id="modify-the-load-balancer-to-serve-https">Modify the Load Balancer to serve HTTPS</h3>
<p>Back in the Elastic Beanstalk console, click "Configuration". Then, within the "Load balancer" category, click "Edit". Click "Add listener" and create a listener with the following details:</p>
<ol>
<li>Port - 443</li>
<li>Protocol - HTTPS</li>
<li>SSL certificate - select the certificate that you just created</li>
</ol>
<li>Port - 443</li>
<li>Protocol - HTTPS</li>
<li>SSL certificate - select the certificate that you just created</li>
<p>Click "Add". Then, scroll to the bottom of the page and click "Apply". It will take a few minutes for the environment to update.</p>
<h3 id="modify-your-application-settings">Modify your Application Settings</h3>
<p>Next, we need to make a few changes to our Django application.</p>
<p>First, add your fully qualified domain to <code>ALLOWED_HOSTS</code>:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">ALLOWED_HOSTS</span> <span class="o">=</span> <span class="p">[</span>
<span class="c1"># ...</span>
<span class="s1">'yourdomain.com'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p>Last, we need to redirect all traffic from HTTP to HTTPS. There are multiple ways of doing this, but the easiest way is to set up <a href="https://httpd.apache.org/">Apache</a> as a proxy host. We can achieve this programmatically by adding the following to the end of the <code>option_settings</code> in <em>.ebextensions/01_django.config</em>:</p>
<pre><span></span><code># .ebextensions/01_django.config

option_settings:
# ...
aws:elasticbeanstalk:environment:proxy:  # new
ProxyServer: apache                    # new
</code></pre>
<p>Your final <em>01_django.config</em> file should now look like this:</p>
<pre><span></span><code><span class="c1"># .ebextensions/01_django.config</span><span class="w"></span>

<span class="n">option_settings</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">application</span><span class="p">:</span><span class="n">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">DJANGO_SETTINGS_MODULE</span><span class="p">:</span><span class="w"> </span><span class="s2">"core.settings"</span><span class="w"></span>
<span class="w">    </span><span class="n">PYTHONPATH</span><span class="p">:</span><span class="w"> </span><span class="s2">"/var/app/current:$PYTHONPATH"</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">container</span><span class="p">:</span><span class="n">python</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">WSGIPath</span><span class="p">:</span><span class="w"> </span><span class="s2">"core.wsgi:application"</span><span class="w"></span>
<span class="w">  </span><span class="n">aws</span><span class="p">:</span><span class="n">elasticbeanstalk</span><span class="p">:</span><span class="n">environment</span><span class="p">:</span><span class="n">proxy</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">ProxyServer</span><span class="p">:</span><span class="w"> </span><span class="n">apache</span><span class="w"></span>

<span class="n">container_commands</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="mi">01</span><span class="n">_makemigrations</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py makemigrations --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">02</span><span class="n">_migrate</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py migrate --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">03</span><span class="n">_superuser</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py createsu"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
<span class="w">  </span><span class="mi">04</span><span class="n">_collectstatic</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="n">command</span><span class="p">:</span><span class="w"> </span><span class="s2">"source /var/app/venv/*/bin/activate &amp;&amp; python3 manage.py collectstatic --noinput"</span><span class="w"></span>
<span class="w">    </span><span class="n">leader_only</span><span class="p">:</span><span class="w"> </span><span class="bp">true</span><span class="w"></span>
</code></pre>
<p>Next, create a ".platform" folder in the project root and add the following files and folders:</p>
<pre><span></span><code>└-- .platform
└-- httpd
└-- conf.d
└-- ssl_rewrite.conf
</code></pre>
<p><em>ssl_rewrite.conf</em>:</p>
<pre><span></span><code># .platform/httpd/conf.d/ssl_rewrite.conf

RewriteEngine On
<span class="nt">&lt;If</span> <span class="err">"-n</span> <span class="err">'%{HTTP:X-Forwarded-Proto}'</span> <span class="err">&amp;&amp;</span> <span class="err">%{HTTP:X-Forwarded-Proto}</span> <span class="err">!=</span> <span class="err">'https'"</span><span class="nt">&gt;</span>
RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [R,L]
<span class="nt">&lt;/If&gt;</span>
</code></pre>
<p>Your project structure should now look like this:</p>
<pre><span></span><code><span class="p">|</span>-- .ebextensions
<span class="p">|</span>   └-- 01_django.config
<span class="p">|</span>-- .elasticbeanstalk
<span class="p">|</span>   └-- config.yml
<span class="p">|</span>-- .gitignore
<span class="p">|</span>-- .platform
<span class="p">|</span>   └-- httpd
<span class="p">|</span>       └-- conf.d
<span class="p">|</span>           └-- ssl_rewrite.conf
<span class="p">|</span>-- README.md
<span class="p">|</span>-- core
<span class="p">|</span>   <span class="p">|</span>-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- asgi.py
<span class="p">|</span>   <span class="p">|</span>-- settings.py
<span class="p">|</span>   <span class="p">|</span>-- urls.py
<span class="p">|</span>   └-- wsgi.py
<span class="p">|</span>-- db.sqlite3
<span class="p">|</span>-- images
<span class="p">|</span>   <span class="p">|</span>-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- admin.py
<span class="p">|</span>   <span class="p">|</span>-- apps.py
<span class="p">|</span>   <span class="p">|</span>-- forms.py
│   ├── management
│   │   ├── __init__.py
│   │   └── commands
│   │       ├── __init__.py
│   │       └── createsu.py
<span class="p">|</span>   <span class="p">|</span>-- migrations
<span class="p">|</span>   <span class="p">|</span>   <span class="p">|</span>-- 0001_initial.py
<span class="p">|</span>   <span class="p">|</span>   └-- __init__.py
<span class="p">|</span>   <span class="p">|</span>-- models.py
<span class="p">|</span>   <span class="p">|</span>-- tables.py
<span class="p">|</span>   <span class="p">|</span>-- templates
<span class="p">|</span>   <span class="p">|</span>   └-- images
<span class="p">|</span>   <span class="p">|</span>       └-- index.html
<span class="p">|</span>   <span class="p">|</span>-- tests.py
<span class="p">|</span>   <span class="p">|</span>-- urls.py
<span class="p">|</span>   └-- views.py
<span class="p">|</span>-- manage.py
└-- requirements.txt
</code></pre>
<p>Commit the changes to git and deploy:</p>
<pre><span></span><code>$ git add .
$ git commit -m <span class="s2">"updates for eb"</span>

$ eb deploy
</code></pre>
<p>Now, in your browser, the <code>https://</code> flavor of your application should work. Try going to the <code>http://</code> flavor. You should be redirected to the <code>https://</code> flavor. Ensure the certificate is loaded properly as well.</p>

<h2 id="environment-variables">Environment Variables</h2>
<p>In production, it's <a href="https://12factor.net/config">best to store environment-specific config in environment variables</a>. With Elastic Beanstalk you can set custom environmental variables two different ways.</p>
<h3 id="environment-variables-via-eb-cli">Environment Variables via EB CLI</h3>
<p>Let's turn Django's <code>SECRET_KEY</code> and <code>DEBUG</code> settings into environmental variables.</p>
<p>Start by running:</p>
<pre><span></span><code>$ eb setenv <span class="nv">DJANGO_SECRET_KEY</span><span class="o">=</span><span class="s1">'&lt;replace me with your own secret key&gt;'</span> <span class="se">\</span>
<span class="nv">DJANGO_DEBUG</span><span class="o">=</span><span class="s1">'1'</span>
</code></pre>
<p>You can set multiple environmental variables with one command by separating them with spaces. This is the recommended approach as it results in only a single update to the EB environment.</p>
<p>Change <em>core/settings.py</em> accordingly:</p>
<pre><span></span><code><span class="c1"># core/settings.py</span>

<span class="n">SECRET_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
<span class="s1">'DJANGO_SECRET_KEY'</span><span class="p">,</span>
<span class="s1">'&lt;replace me with your own fallback secret key&gt;'</span>
<span class="p">)</span>

<span class="n">DEBUG</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">'DJANGO_DEBUG'</span><span class="p">,</span> <span class="s1">'1'</span><span class="p">)</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">'true'</span><span class="p">,</span> <span class="s1">'t'</span><span class="p">,</span> <span class="s1">'1'</span><span class="p">]</span>
</code></pre>
<p>Commit the changes to git and deploy:</p>
<pre><span></span><code>$ git add .
$ git commit -m <span class="s2">"updates for eb"</span>

$ eb deploy
</code></pre>
<h3 id="environment-variables-via-eb-console">Environment Variables via EB Console</h3>
<p>Enter the Elastic Beanstalk console via <code>eb open</code>. Navigate to "Configuration" &gt; "Software" &gt; "Edit". Then, scroll down to the "Environment properties".</p>


<p>After you're done, click "Apply" and your environment will update.</p>
<p>You can then access these variables in your Python environment via <code>os.environ</code>.</p>
<p>For example:</p>
<pre><span></span><code><span class="n">VARIABLE_NAME</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">environ</span><span class="p">[</span><span class="s1">'VARIABLE_NAME'</span><span class="p">]</span>
</code></pre>
<h2 id="debugging-elastic-beanstalk">Debugging Elastic Beanstalk</h2>
<p>When working with Elastic Beanstalk, it can be pretty frustrating to figure out what went wrong if you don't know how to access the log files. In this section will look at just that.</p>
<p>There are two ways to access the logs:</p>
<ol>
<li>Elastic Beanstalk CLI or console</li>
<li>SSH into EC2 instance</li>
</ol>
<li>Elastic Beanstalk CLI or console</li>
<li>SSH into EC2 instance</li>
<p>From personal experience, I've been able to solve all issues with the first approach.</p>
<h3 id="elastic-beanstalk-cli-or-console">Elastic Beanstalk CLI or Console</h3>
<p>CLI:</p>
<pre><span></span><code>$ eb logs
</code></pre>
<p>This command will fetch the last 100 lines from the following files:</p>
<pre><span></span><code><span class="o">/</span><span class="k">var</span><span class="o">/</span><span class="nb">log</span><span class="o">/</span><span class="n">web</span><span class="o">.</span><span class="n">stdout</span><span class="o">.</span><span class="n">log</span><span class="w"></span>
<span class="o">/</span><span class="k">var</span><span class="o">/</span><span class="nb">log</span><span class="o">/</span><span class="n">eb</span><span class="o">-</span><span class="n">hooks</span><span class="o">.</span><span class="n">log</span><span class="w"></span>
<span class="o">/</span><span class="k">var</span><span class="o">/</span><span class="nb">log</span><span class="o">/</span><span class="n">nginx</span><span class="o">/</span><span class="n">access</span><span class="o">.</span><span class="n">log</span><span class="w"></span>
<span class="o">/</span><span class="k">var</span><span class="o">/</span><span class="nb">log</span><span class="o">/</span><span class="n">nginx</span><span class="o">/</span><span class="n">error</span><span class="o">.</span><span class="n">log</span><span class="w"></span>
<span class="o">/</span><span class="k">var</span><span class="o">/</span><span class="nb">log</span><span class="o">/</span><span class="n">eb</span><span class="o">-</span><span class="n">engine</span><span class="o">.</span><span class="n">log</span><span class="w"></span>
</code></pre>
<p>Running <code>eb logs</code> is equivalent to logging into the EB console and navigating to "Logs".</p>
<p>I recommend piping the logs to <a href="https://aws.amazon.com/cloudwatch/">CloudWatch</a>. Run the following command to enable this:</p>
<pre><span></span><code>$ eb logs --cloudwatch-logs <span class="nb">enable</span>
</code></pre>
<p>You'll typically find Django errors in <em>/var/log/web.stdout.log</em> or <em>/var/log/eb-engine.log</em>.</p>
<p>To learn more about Elastic Beanstalk logs check out <a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html">Viewing logs from Amazon EC2 instances</a>.</p>
<h3 id="ssh-into-ec2-instance">SSH into EC2 Instance</h3>
<p>To connect to an EC2 instance where your Django application is running, run:</p>
<pre><span></span><code>$ eb ssh
</code></pre>


