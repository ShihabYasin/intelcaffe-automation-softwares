
<h1>Storing Django Static and Media Files on Amazon S3</h1>

<h2 id="s3-bucket">S3 Bucket</h2>
<p>Before beginning, you will need an <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/sign-up-for-aws.html">AWS</a> account. If you’re new to AWS, Amazon provides a <a href="https://aws.amazon.com/free/">free tier</a> with 5GB of S3 storage.</p>
<p>To create an <a href="https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html">S3 bucket</a>, navigate to the <a href="https://console.aws.amazon.com/s3">S3 page</a> and click "Create bucket":</p>
<p><not_img alt="aws s3" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_s3_1.png" loading="lazy" style="max-width:100%"/></p>
<p>Give the bucket a <a href="https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html">unique, DNS-compliant name</a> and select a <a href="https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region">region</a>:</p>
<p><not_img alt="aws s3" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_s3_2.png" loading="lazy" style="max-width:100%"/></p>
<p>Turn off "Block all public access":</p>
<p><not_img alt="aws s3" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_s3_5.png" loading="lazy" style="max-width:100%"/></p>
<p>Create the bucket. You should now see your bucket back on the main S3 page:</p>
<p><not_img alt="aws s3" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_s3_3.png" loading="lazy" style="max-width:100%"/></p>
<h2 id="iam-access">IAM Access</h2>
<p>Although you could use the AWS root user, it's best for security to create an IAM user that only has access to S3 or to a specific S3 bucket. What's more, by setting up a group, it makes it much easier to assign (and remove) access to the bucket. So, we'll start by setting up a group with limited <a href="https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-access-control.html">permissions</a> and then create a user and assign that user to the group.</p>
<h3 id="iam-group">IAM Group</h3>
<p>Within the <a href="https://console.aws.amazon.com/">AWS Console</a>, navigate to the main <a href="https://console.aws.amazon.com/iam">IAM page</a> and click "User groups" on the sidebar. Then, click the "Create group" button, provide a name for the group and then search for and select the built-in policy "AmazonS3FullAccess":</p>
<p><not_img alt="aws iam" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_iam_1.png" loading="lazy" style="max-width:100%"/></p>
<p>Click "Create Group" to finish setting up the group:</p>
<p><not_img alt="aws iam" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_iam_2.png" loading="lazy" style="max-width:100%"/></p>
<p>If you'd like to limit access even more, to the specific bucket we just created, create a new policy with the following permissions:
</p>
<pre><span></span><span class="p">{</span>
<span class="nt">"Version"</span><span class="p">:</span> <span class="s2">"2012-10-17"</span><span class="p">,</span>
<span class="nt">"Statement"</span><span class="p">:</span> <span class="p">[</span>
<span class="p">{</span>
<span class="nt">"Effect"</span><span class="p">:</span> <span class="s2">"Allow"</span><span class="p">,</span>
<span class="nt">"Action"</span><span class="p">:</span> <span class="s2">"s3:*"</span><span class="p">,</span>
<span class="nt">"Resource"</span><span class="p">:</span> <span class="p">[</span>
<span class="s2">"arn:aws:s3:::your-bucket-name"</span><span class="p">,</span>
<span class="s2">"arn:aws:s3:::your-bucket-name/*"</span>
<span class="p">]</span>
<span class="p">}</span>
<span class="p">]</span>
<span class="p">}</span>
</pre>
<p>Be sure to replace <code>your-bucket-name</code> with the actual name. Then, detach the "AmazonS3FullAccess" policy from the group and attach the new policy.</p>
<h3 id="iam-user">IAM User</h3>
<p>Back on the main <a href="https://console.aws.amazon.com/iam">IAM page</a>, click "Users" and then "Add user". Define a user name and select "Programmatic access" under the "Access type":</p>
<p><not_img alt="aws iam" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_iam_3.png" loading="lazy" style="max-width:100%"/></p>
<p>Click the next button to move on to the "Permissions" step. Select the group we just created:</p>
<p><not_img alt="aws iam" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_iam_4.png" loading="lazy" style="max-width:100%"/></p>
<p>Click next again a few times until you're at the "Review" step. Click "Create user" to create the new user. You should now see the user's access key ID and secret access key:</p>
<p><not_img alt="aws iam" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_iam_5.png" loading="lazy" style="max-width:100%"/></p>
<p>Take note of the keys.</p>
<h2 id="django-project">Django Project</h2>
<p>Clone down the <a href="https://github.com/ShihabYasin/django-amazon-s3-media-files</a> repo, and then check out the <a href="https://github.com/testdrivenio/django-docker-s3/releases/tag/v1">v1</a> tag to the master branch:</p>
<pre><span></span><code>$ git clone https://github.com/testdrivenio/django-docker-s3 --branch v1 --single-branch
$ <span class="nb">cd</span> django-docker-s3
$ git checkout tags/v1 -b master
</code></pre>
<p>From the project root, create the images and spin up the Docker containers:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<p>Once the build is complete, collect the static files:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py collectstatic
</code></pre>
<p>Then, navigate to <a href="http://localhost:1337">http://localhost:1337</a>:</p>
<p><not_img alt="app" class="lazyload" data-src="/static/images/blog/django/django-s3/app.png" loading="lazy" style="max-width:100%"/></p>
<p>You should be able to upload an image, and then view the image at <a href="http://localhost:1337/mediafiles/IMAGE_FILE_NAME">http://localhost:1337/mediafiles/IMAGE_FILE_NAME</a>.</p>
<p>The radio buttons, for public vs. private, do not work. We'll be adding this functionality later in this tutorial. Ignore them for now.</p>
<p>Take a quick look at the project structure before moving on:</p>
<pre><span></span><code>├── .gitignore
├── LICENSE
├── README.md
├── app
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── hello_django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── mediafiles
│   ├── requirements.txt
│   ├── static
│   │   └── bulma.min.css
│   ├── staticfiles
│   └── upload
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations
│       │   └── __init__.py
│       ├── models.py
│       ├── templates
│       │   └── upload.html
│       ├── tests.py
│       └── views.py
├── docker-compose.yml
└── nginx
├── Dockerfile
└── nginx.conf
</code></pre>


<h2 id="django-storages">Django Storages</h2>
<p>Next, install <a href="https://django-storages.readthedocs.io">django-storages</a>, to use S3 as the main Django storage backend, and <a href="https://boto3.readthedocs.io/">boto3</a>, to interact with the AWS API.</p>
<p>Update the requirements file:</p>
<pre><span></span><code>boto3==1.17.58
Django==3.2
django-storages==1.11.1
gunicorn==20.1.0
</code></pre>
<p>Add <code>storages</code> to the <code>INSTALLED_APPS</code> in <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">INSTALLED_APPS</span> <span class="o">=</span> <span class="p">[</span>
<span class="s1">'django.contrib.admin'</span><span class="p">,</span>
<span class="s1">'django.contrib.auth'</span><span class="p">,</span>
<span class="s1">'django.contrib.contenttypes'</span><span class="p">,</span>
<span class="s1">'django.contrib.sessions'</span><span class="p">,</span>
<span class="s1">'django.contrib.messages'</span><span class="p">,</span>
<span class="s1">'django.contrib.staticfiles'</span><span class="p">,</span>
<span class="s1">'upload'</span><span class="p">,</span>
<span class="s1">'storages'</span><span class="p">,</span>
<span class="p">]</span>
</code></pre>
<p>Update the images and spin up the new containers:</p>
<pre><span></span><code>$ docker-compose up -d --build
</code></pre>
<h2 id="static-files">Static Files</h2>
<p>Moving along, we need to update the handling of static files in <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">STATIC_URL</span> <span class="o">=</span> <span class="s1">'/staticfiles/'</span>
<span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'staticfiles'</span><span class="p">)</span>
<span class="n">STATICFILES_DIRS</span> <span class="o">=</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'static'</span><span class="p">),)</span>


<span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s1">'/mediafiles/'</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'mediafiles'</span><span class="p">)</span>
</code></pre>
<p>Replace those settings with the following:</p>
<pre><span></span><code><span class="n">USE_S3</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'USE_S3'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'TRUE'</span>

<span class="k">if</span> <span class="n">USE_S3</span><span class="p">:</span>
<span class="c1"># aws settings</span>
<span class="n">AWS_ACCESS_KEY_ID</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_ACCESS_KEY_ID'</span><span class="p">)</span>
<span class="n">AWS_SECRET_ACCESS_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_SECRET_ACCESS_KEY'</span><span class="p">)</span>
<span class="n">AWS_STORAGE_BUCKET_NAME</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_STORAGE_BUCKET_NAME'</span><span class="p">)</span>
<span class="n">AWS_DEFAULT_ACL</span> <span class="o">=</span> <span class="s1">'public-read'</span>
<span class="n">AWS_S3_CUSTOM_DOMAIN</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="n">AWS_STORAGE_BUCKET_NAME</span><span class="si">}</span><span class="s1">.s3.amazonaws.com'</span>
<span class="n">AWS_S3_OBJECT_PARAMETERS</span> <span class="o">=</span> <span class="p">{</span><span class="s1">'CacheControl'</span><span class="p">:</span> <span class="s1">'max-age=86400'</span><span class="p">}</span>
<span class="c1"># s3 static settings</span>
<span class="n">AWS_LOCATION</span> <span class="o">=</span> <span class="s1">'static'</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'https://</span><span class="si">{</span><span class="n">AWS_S3_CUSTOM_DOMAIN</span><span class="si">}</span><span class="s1">/</span><span class="si">{</span><span class="n">AWS_LOCATION</span><span class="si">}</span><span class="s1">/'</span>
<span class="n">STATICFILES_STORAGE</span> <span class="o">=</span> <span class="s1">'storages.backends.s3boto3.S3Boto3Storage'</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="s1">'/staticfiles/'</span>
<span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'staticfiles'</span><span class="p">)</span>

<span class="n">STATICFILES_DIRS</span> <span class="o">=</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'static'</span><span class="p">),)</span>

<span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s1">'/mediafiles/'</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'mediafiles'</span><span class="p">)</span>
</code></pre>
<p>Take note of <code>USE_S3</code> and <code>STATICFILES_STORAGE</code>:</p>
<ol>
<li>The <code>USE_S3</code> environment variable is used to turn the S3 storage on (value is <code>TRUE</code>) and off (value is <code>FALSE</code>). So, you could configure two Docker compose files: one for development with S3 off and the other for production with S3 on.</li>
<li>The <code>STATICFILES_STORAGE</code> <a href="https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html?highlight=STATICFILES_STORAGE">setting</a> configures Django to automatically add static files to the S3 bucket when the <code>collectstatic</code> command is run.</li>
</ol>
<li>The <code>USE_S3</code> environment variable is used to turn the S3 storage on (value is <code>TRUE</code>) and off (value is <code>FALSE</code>). So, you could configure two Docker compose files: one for development with S3 off and the other for production with S3 on.</li>
<li>The <code>STATICFILES_STORAGE</code> <a href="https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html?highlight=STATICFILES_STORAGE">setting</a> configures Django to automatically add static files to the S3 bucket when the <code>collectstatic</code> command is run.</li>
<p>Review the <a href="https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html">official django-storages documentation</a> for more info on the above settings and config.</p>
<p>Add the appropriate environment variables to the <code>web</code> service in the <em>docker-compose.yml</em> file:</p>
<pre><span></span><code><span class="nt">web</span><span class="p">:</span><span class="w"></span>
<span class="w">  </span><span class="nt">build</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app</span><span class="w"></span>
<span class="w">  </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">bash -c 'while !&lt;/dev/tcp/db/5432; do sleep 1; done; gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000'</span><span class="w"></span>
<span class="w">  </span><span class="nt">volumes</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">./app/:/usr/src/app/</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">static_volume:/usr/src/app/staticfiles</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">media_volume:/usr/src/app/mediafiles</span><span class="w"></span>
<span class="w">  </span><span class="nt">expose</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">8000</span><span class="w"></span>
<span class="w">  </span><span class="nt">environment</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SECRET_KEY=please_change_me</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SQL_ENGINE=django.db.backends.postgresql</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SQL_DATABASE=postgres</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SQL_USER=postgres</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SQL_PASSWORD=postgres</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SQL_HOST=db</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">SQL_PORT=5432</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">DATABASE=postgres</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">USE_S3=TRUE</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">AWS_ACCESS_KEY_ID=UPDATE_ME</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">AWS_SECRET_ACCESS_KEY=UPDATE_ME</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">AWS_STORAGE_BUCKET_NAME=UPDATE_ME</span><span class="w"></span>
<span class="w">  </span><span class="nt">depends_on</span><span class="p">:</span><span class="w"></span>
<span class="w">    </span><span class="p p-Indicator">-</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">db</span><span class="w"></span>
</code></pre>
<p>Don't forget to update <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code> with the user keys that you just created along with the <code>AWS_STORAGE_BUCKET_NAME</code>.</p>
<p>To test, re-build and run the containers:</p>
<pre><span></span><code>$ docker-compose down -v
$ docker-compose up -d --build
</code></pre>
<p>Collect the static files:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py collectstatic
</code></pre>
<p>It should take much longer than before since the files are being uploaded to the S3 bucket.</p>
<p><a href="http://localhost:1337">http://localhost:1337</a> should still render correctly:</p>
<p><not_img alt="app" class="lazyload" data-src="/static/images/blog/django/django-s3/app.png" loading="lazy" style="max-width:100%"/></p>
<p>View the page source to ensure the CSS stylesheet is pulled in from the S3 bucket:</p>
<p><not_img alt="app" class="lazyload" data-src="/static/images/blog/django/django-s3/app_2.png" loading="lazy" style="max-width:100%"/></p>
<p>Verify that the static files can be seen on the AWS console within the "static" subfolder of the S3 bucket:</p>
<p><not_img alt="aws s3" class="lazyload" data-src="/static/images/blog/django/django-s3/aws_s3_4.png" loading="lazy" style="max-width:100%"/></p>
<p>Media uploads will still hit the local filesystem since we've only configured S3 for static files. We'll work with media uploads shortly.</p>
<p>Finally, update the value of <code>USE_S3</code> to <code>FALSE</code> and re-build the images to make sure that Django uses the local filesystem for static files. Once done, change <code>USE_S3</code> back to <code>TRUE</code>.</p>
<h2 id="public-media-files">Public Media Files</h2>
<p>To prevent users from overwriting existing static files, media file uploads should be placed in a different subfolder in the bucket. We'll handle this by creating custom storage classes for each type of storage.</p>
<p>Add a new file called <em>storage_backends.py</em> to the "app/hello_django" folder:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">storages.backends.s3boto3</span> <span class="kn">import</span> <span class="n">S3Boto3Storage</span>


<span class="k">class</span> <span class="nc">StaticStorage</span><span class="p">(</span><span class="n">S3Boto3Storage</span><span class="p">):</span>
<span class="n">location</span> <span class="o">=</span> <span class="s1">'static'</span>
<span class="n">default_acl</span> <span class="o">=</span> <span class="s1">'public-read'</span>


<span class="k">class</span> <span class="nc">PublicMediaStorage</span><span class="p">(</span><span class="n">S3Boto3Storage</span><span class="p">):</span>
<span class="n">location</span> <span class="o">=</span> <span class="s1">'media'</span>
<span class="n">default_acl</span> <span class="o">=</span> <span class="s1">'public-read'</span>
<span class="n">file_overwrite</span> <span class="o">=</span> <span class="kc">False</span>
</code></pre>
<p>Make the following changes to <em>settings.py</em>:</p>
<pre><span></span><code><span class="n">USE_S3</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'USE_S3'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'TRUE'</span>

<span class="k">if</span> <span class="n">USE_S3</span><span class="p">:</span>
<span class="c1"># aws settings</span>
<span class="n">AWS_ACCESS_KEY_ID</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_ACCESS_KEY_ID'</span><span class="p">)</span>
<span class="n">AWS_SECRET_ACCESS_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_SECRET_ACCESS_KEY'</span><span class="p">)</span>
<span class="n">AWS_STORAGE_BUCKET_NAME</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_STORAGE_BUCKET_NAME'</span><span class="p">)</span>
<span class="n">AWS_DEFAULT_ACL</span> <span class="o">=</span> <span class="kc">None</span>
<span class="n">AWS_S3_CUSTOM_DOMAIN</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="n">AWS_STORAGE_BUCKET_NAME</span><span class="si">}</span><span class="s1">.s3.amazonaws.com'</span>
<span class="n">AWS_S3_OBJECT_PARAMETERS</span> <span class="o">=</span> <span class="p">{</span><span class="s1">'CacheControl'</span><span class="p">:</span> <span class="s1">'max-age=86400'</span><span class="p">}</span>
<span class="c1"># s3 static settings</span>
<span class="n">STATIC_LOCATION</span> <span class="o">=</span> <span class="s1">'static'</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'https://</span><span class="si">{</span><span class="n">AWS_S3_CUSTOM_DOMAIN</span><span class="si">}</span><span class="s1">/</span><span class="si">{</span><span class="n">STATIC_LOCATION</span><span class="si">}</span><span class="s1">/'</span>
<span class="n">STATICFILES_STORAGE</span> <span class="o">=</span> <span class="s1">'hello_django.storage_backends.StaticStorage'</span>
<span class="c1"># s3 public media settings</span>
<span class="n">PUBLIC_MEDIA_LOCATION</span> <span class="o">=</span> <span class="s1">'media'</span>
<span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'https://</span><span class="si">{</span><span class="n">AWS_S3_CUSTOM_DOMAIN</span><span class="si">}</span><span class="s1">/</span><span class="si">{</span><span class="n">PUBLIC_MEDIA_LOCATION</span><span class="si">}</span><span class="s1">/'</span>
<span class="n">DEFAULT_FILE_STORAGE</span> <span class="o">=</span> <span class="s1">'hello_django.storage_backends.PublicMediaStorage'</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="s1">'/staticfiles/'</span>
<span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'staticfiles'</span><span class="p">)</span>
<span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s1">'/mediafiles/'</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'mediafiles'</span><span class="p">)</span>

<span class="n">STATICFILES_DIRS</span> <span class="o">=</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'static'</span><span class="p">),)</span>
</code></pre>
<p>With the <code>DEFAULT_FILE_STORAGE</code> <a href="https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html?highlight=DEFAULT_FILE_STORAGE">setting</a> now set, all <a href="https://docs.djangoproject.com/en/3.0/ref/models/fields/#filefield">FileField</a>s will upload their content to the S3 bucket. Review the remaining settings before moving on.</p>
<p>Next, let's make a few changes to the <code>upload</code> app.</p>
<p><em>app/upload/models.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>


<span class="k">class</span> <span class="nc">Upload</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">uploaded_at</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">file</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">FileField</span><span class="p">()</span>
</code></pre>
<p><em>app/upload/views.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">django.core.files.storage</span> <span class="kn">import</span> <span class="n">FileSystemStorage</span>
<span class="kn">from</span> <span class="nn">django.shortcuts</span> <span class="kn">import</span> <span class="n">render</span>

<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">Upload</span>


<span class="k">def</span> <span class="nf">image_upload</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s1">'POST'</span><span class="p">:</span>
<span class="n">image_file</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">FILES</span><span class="p">[</span><span class="s1">'image_file'</span><span class="p">]</span>
<span class="n">image_type</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">POST</span><span class="p">[</span><span class="s1">'image_type'</span><span class="p">]</span>
<span class="k">if</span> <span class="n">settings</span><span class="o">.</span><span class="n">USE_S3</span><span class="p">:</span>
<span class="n">upload</span> <span class="o">=</span> <span class="n">Upload</span><span class="p">(</span><span class="n">file</span><span class="o">=</span><span class="n">image_file</span><span class="p">)</span>
<span class="n">upload</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
<span class="n">image_url</span> <span class="o">=</span> <span class="n">upload</span><span class="o">.</span><span class="n">file</span><span class="o">.</span><span class="n">url</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">fs</span> <span class="o">=</span> <span class="n">FileSystemStorage</span><span class="p">()</span>
<span class="n">filename</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">save</span><span class="p">(</span><span class="n">image_file</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="n">image_file</span><span class="p">)</span>
<span class="n">image_url</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">url</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'upload.html'</span><span class="p">,</span> <span class="p">{</span>
<span class="s1">'image_url'</span><span class="p">:</span> <span class="n">image_url</span>
<span class="p">})</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'upload.html'</span><span class="p">)</span>
</code></pre>
<p>Create the new migration file and then build the new images:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py makemigrations
$ docker-compose down -v
$ docker-compose up -d --build
$ docker-compose <span class="nb">exec</span> web python manage.py migrate
</code></pre>
<p>Test it out! Upload an image at <a href="http://localhost:1337">http://localhost:1337</a>. The image should be uploaded to S3 (to the media subfolder) and the <code>image_url</code> should include the S3 url:</p>
<p><not_img alt="app demo" class="lazyload" data-src="/static/images/gifs/blog/django-s3/public-media.gif" loading="lazy" style="max-width:100%"/></p>
<h2 id="private-media-files">Private Media Files</h2>
<p>Add a new class to the <em>storage_backends.py</em>:</p>
<pre><span></span><code><span class="k">class</span> <span class="nc">PrivateMediaStorage</span><span class="p">(</span><span class="n">S3Boto3Storage</span><span class="p">):</span>
<span class="n">location</span> <span class="o">=</span> <span class="s1">'private'</span>
<span class="n">default_acl</span> <span class="o">=</span> <span class="s1">'private'</span>
<span class="n">file_overwrite</span> <span class="o">=</span> <span class="kc">False</span>
<span class="n">custom_domain</span> <span class="o">=</span> <span class="kc">False</span>
</code></pre>
<p>Add the appropriate settings:</p>
<pre><span></span><code><span class="n">USE_S3</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'USE_S3'</span><span class="p">)</span> <span class="o">==</span> <span class="s1">'TRUE'</span>

<span class="k">if</span> <span class="n">USE_S3</span><span class="p">:</span>
<span class="c1"># aws settings</span>
<span class="n">AWS_ACCESS_KEY_ID</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_ACCESS_KEY_ID'</span><span class="p">)</span>
<span class="n">AWS_SECRET_ACCESS_KEY</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_SECRET_ACCESS_KEY'</span><span class="p">)</span>
<span class="n">AWS_STORAGE_BUCKET_NAME</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">'AWS_STORAGE_BUCKET_NAME'</span><span class="p">)</span>
<span class="n">AWS_DEFAULT_ACL</span> <span class="o">=</span> <span class="kc">None</span>
<span class="n">AWS_S3_CUSTOM_DOMAIN</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'</span><span class="si">{</span><span class="n">AWS_STORAGE_BUCKET_NAME</span><span class="si">}</span><span class="s1">.s3.amazonaws.com'</span>
<span class="n">AWS_S3_OBJECT_PARAMETERS</span> <span class="o">=</span> <span class="p">{</span><span class="s1">'CacheControl'</span><span class="p">:</span> <span class="s1">'max-age=86400'</span><span class="p">}</span>
<span class="c1"># s3 static settings</span>
<span class="n">STATIC_LOCATION</span> <span class="o">=</span> <span class="s1">'static'</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'https://</span><span class="si">{</span><span class="n">AWS_S3_CUSTOM_DOMAIN</span><span class="si">}</span><span class="s1">/</span><span class="si">{</span><span class="n">STATIC_LOCATION</span><span class="si">}</span><span class="s1">/'</span>
<span class="n">STATICFILES_STORAGE</span> <span class="o">=</span> <span class="s1">'hello_django.storage_backends.StaticStorage'</span>
<span class="c1"># s3 public media settings</span>
<span class="n">PUBLIC_MEDIA_LOCATION</span> <span class="o">=</span> <span class="s1">'media'</span>
<span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">'https://</span><span class="si">{</span><span class="n">AWS_S3_CUSTOM_DOMAIN</span><span class="si">}</span><span class="s1">/</span><span class="si">{</span><span class="n">PUBLIC_MEDIA_LOCATION</span><span class="si">}</span><span class="s1">/'</span>
<span class="n">DEFAULT_FILE_STORAGE</span> <span class="o">=</span> <span class="s1">'hello_django.storage_backends.PublicMediaStorage'</span>
<span class="c1"># s3 private media settings</span>
<span class="n">PRIVATE_MEDIA_LOCATION</span> <span class="o">=</span> <span class="s1">'private'</span>
<span class="n">PRIVATE_FILE_STORAGE</span> <span class="o">=</span> <span class="s1">'hello_django.storage_backends.PrivateMediaStorage'</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">STATIC_URL</span> <span class="o">=</span> <span class="s1">'/staticfiles/'</span>
<span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'staticfiles'</span><span class="p">)</span>
<span class="n">MEDIA_URL</span> <span class="o">=</span> <span class="s1">'/mediafiles/'</span>
<span class="n">MEDIA_ROOT</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'mediafiles'</span><span class="p">)</span>

<span class="n">STATICFILES_DIRS</span> <span class="o">=</span> <span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">BASE_DIR</span><span class="p">,</span> <span class="s1">'static'</span><span class="p">),)</span>
</code></pre>
<p>Create a new model in <em>app/upload/models.py</em>:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>

<span class="kn">from</span> <span class="nn">hello_django.storage_backends</span> <span class="kn">import</span> <span class="n">PublicMediaStorage</span><span class="p">,</span> <span class="n">PrivateMediaStorage</span>


<span class="k">class</span> <span class="nc">Upload</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">uploaded_at</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">file</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">FileField</span><span class="p">(</span><span class="n">storage</span><span class="o">=</span><span class="n">PublicMediaStorage</span><span class="p">())</span>


<span class="k">class</span> <span class="nc">UploadPrivate</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
<span class="n">uploaded_at</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateTimeField</span><span class="p">(</span><span class="n">auto_now_add</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<span class="n">file</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">FileField</span><span class="p">(</span><span class="n">storage</span><span class="o">=</span><span class="n">PrivateMediaStorage</span><span class="p">())</span>
</code></pre>
<p>Then, update the view:</p>
<pre><span></span><code><span class="kn">from</span> <span class="nn">django.conf</span> <span class="kn">import</span> <span class="n">settings</span>
<span class="kn">from</span> <span class="nn">django.core.files.storage</span> <span class="kn">import</span> <span class="n">FileSystemStorage</span>
<span class="kn">from</span> <span class="nn">django.shortcuts</span> <span class="kn">import</span> <span class="n">render</span>

<span class="kn">from</span> <span class="nn">.models</span> <span class="kn">import</span> <span class="n">Upload</span><span class="p">,</span> <span class="n">UploadPrivate</span>


<span class="k">def</span> <span class="nf">image_upload</span><span class="p">(</span><span class="n">request</span><span class="p">):</span>
<span class="k">if</span> <span class="n">request</span><span class="o">.</span><span class="n">method</span> <span class="o">==</span> <span class="s1">'POST'</span><span class="p">:</span>
<span class="n">image_file</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">FILES</span><span class="p">[</span><span class="s1">'image_file'</span><span class="p">]</span>
<span class="n">image_type</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="n">POST</span><span class="p">[</span><span class="s1">'image_type'</span><span class="p">]</span>
<span class="k">if</span> <span class="n">settings</span><span class="o">.</span><span class="n">USE_S3</span><span class="p">:</span>
<span class="k">if</span> <span class="n">image_type</span> <span class="o">==</span> <span class="s1">'private'</span><span class="p">:</span>
<span class="n">upload</span> <span class="o">=</span> <span class="n">UploadPrivate</span><span class="p">(</span><span class="n">file</span><span class="o">=</span><span class="n">image_file</span><span class="p">)</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">upload</span> <span class="o">=</span> <span class="n">Upload</span><span class="p">(</span><span class="n">file</span><span class="o">=</span><span class="n">image_file</span><span class="p">)</span>
<span class="n">upload</span><span class="o">.</span><span class="n">save</span><span class="p">()</span>
<span class="n">image_url</span> <span class="o">=</span> <span class="n">upload</span><span class="o">.</span><span class="n">file</span><span class="o">.</span><span class="n">url</span>
<span class="k">else</span><span class="p">:</span>
<span class="n">fs</span> <span class="o">=</span> <span class="n">FileSystemStorage</span><span class="p">()</span>
<span class="n">filename</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">save</span><span class="p">(</span><span class="n">image_file</span><span class="o">.</span><span class="n">name</span><span class="p">,</span> <span class="n">image_file</span><span class="p">)</span>
<span class="n">image_url</span> <span class="o">=</span> <span class="n">fs</span><span class="o">.</span><span class="n">url</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'upload.html'</span><span class="p">,</span> <span class="p">{</span>
<span class="s1">'image_url'</span><span class="p">:</span> <span class="n">image_url</span>
<span class="p">})</span>
<span class="k">return</span> <span class="n">render</span><span class="p">(</span><span class="n">request</span><span class="p">,</span> <span class="s1">'upload.html'</span><span class="p">)</span>
</code></pre>
<p>Again, create the migration file, re-build the images, and spin up the new containers:</p>
<pre><span></span><code>$ docker-compose <span class="nb">exec</span> web python manage.py makemigrations
$ docker-compose down -v
$ docker-compose up -d --build
$ docker-compose <span class="nb">exec</span> web python manage.py migrate
</code></pre>
<p>To test, upload a private image at <a href="http://localhost:1337">http://localhost:1337</a>. Like a public image, the image should be uploaded to S3 (to the private subfolder) and the <code>image_url</code> should include the S3 URL along with the following query string parameters:</p>
<ol>
<li>AWSAccessKeyId</li>
<li>Signature</li>
<li>Expires</li>
</ol>
<li>AWSAccessKeyId</li>
<li>Signature</li>
<li>Expires</li>
<p>Essentially, we created a temporary, signed URL that users can access for a specific period of time. You won't be able to access it directly, without the parameters.</p>


