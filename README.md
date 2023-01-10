What is this tool for? <br>
This tool allows you to delete projects in bulk within Snyk by specifying a set of organazations and types of projects to delete<br>

Installation instructions<br>
Clone this repo and run <pre><code>pip -r requirements.txt</pre></code><br>

How do I use this tool? <br>
Within the cloned repo run <pre><code>python3 snyk-bulk-delete.py (add flags here)</code></pre><br> add the necessary flags listed below <br>

<pre><code>
--help/-h : Returns this page \n--orgs/-o : A set of orgs upon which to perform delete (use ! for all orgs<br>
--scatypes : Defines SCA type/s of projects to deletes<br>
--products : Defines product/s types of projects to delete<br>
 * Please replace spaces with dashes(-) when entering orgs <br>
 * If entering multiple values use the following format: "value-1 value-2 value-3"
</code></pre>

Example where all npm and container projects are deleted within test org 1 and test org 2<br>
<pre><code>python3 snyk-bulk-delete.py --orgs "test-org-1 test-org-2" --products=container --scatypes=npm
</code></pre>



