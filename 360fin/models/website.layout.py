<?xml version="1.0"?>
<t name="Main layout" t-name="website.layout">
    <t t-call="web.layout">
        <t t-set="html_data" t-value="{             'lang': lang and lang.replace('_', '-'),             'data-website-id': website.id if (editable or translatable) and website else None,             'data-editable': '1' if editable else None,             'data-translatable': '1' if translatable else None,             'data-edit_translations': '1' if edit_translations else None,             'data-view-xmlid': xmlid if editable or translatable else None,             'data-main-object': repr(main_object) if editable or translatable else None,             'data-oe-company-name': res_company.name         }"/>
        <t t-if="not title">
            <t t-if="not additional_title and main_object and 'name' in main_object">
                <t t-set="additional_title" t-value="main_object.name"/>
            </t>
            <t t-if="main_object and 'website_meta_title' in main_object and main_object.website_meta_title">
                <t t-set="title" t-value="main_object.website_meta_title"/>
            </t>
            <t t-else="">
                <t t-set="title"><t t-if="additional_title"><t t-raw="additional_title"/> | </t><t t-esc="(website or res_company).name"/></t>
            </t>
        </t>
        <t t-set="x_icon" t-value="'/web/image/website/%s/favicon/' % website.id"/>
        <t t-set="head_website">
            <meta name="description" t-att-content="main_object and 'website_meta_description' in main_object                 and main_object.website_meta_description or website_meta_description"/>
            <meta name="keywords" t-att-content="main_object and 'website_meta_keywords' in main_object                 and main_object.website_meta_keywords or website_meta_keywords"/>
            <meta name="generator" content="Odoo"/>

            <!-- OpenGraph tags for Facebook sharing -->
            <meta property="og:title" t-att-content="additional_title"/>
            <meta property="og:site_name" t-att-content="res_company.name"/>
            <t t-if="main_object and 'plain_content' in main_object and main_object.plain_content">
                <t t-set="og_description" t-value="main_object.plain_content[0:500]"/>
                <meta property="og:description" t-att-content="og_description"/>
                <meta property="og:image" t-att-content="request.httprequest.url_root+'logo.png'"/>
                <meta property="og:url" t-att-content="request.httprequest.url_root+request.httprequest.path[1:end]"/>
            </t>

            <t t-set="languages" t-value="website.get_languages() if website else None"/>
            <t t-if="request and request.website_multilang and website">
                <t t-foreach="website.get_alternate_languages(request.httprequest)" t-as="lg">
                    <link rel="alternate" t-att-hreflang="lg['hreflang']" t-att-href="lg['href']"/>
                </t>
            </t>

            <script type="text/javascript">
                odoo.session_info = {
                    is_superuser: <t t-esc="json.dumps(request.env.user._is_superuser())"/>,
                    is_frontend: true,
                };
            </script>

            <t t-call-assets="web.assets_common" t-js="false"/>
            <t t-call-assets="web.assets_frontend" t-js="false"/>
            <t t-call-assets="web_editor.summernote" t-js="false" groups="website.group_website_publisher"/>
            <t t-call-assets="web_editor.assets_editor" t-js="false" groups="website.group_website_publisher"/>
            <t t-call-assets="website.assets_editor" t-js="false" groups="website.group_website_publisher"/>

            <t t-call-assets="web.assets_common" t-css="false"/>
            <t t-call-assets="web.assets_frontend" t-css="false"/>
            <t t-call-assets="web_editor.summernote" t-css="false" groups="website.group_website_publisher"/>
            <t t-call-assets="web_editor.assets_editor" t-css="false" groups="website.group_website_publisher"/>
            <t t-call-assets="website.assets_editor" t-css="false" groups="website.group_website_publisher"/>
        </t>
        <t t-set="head" t-value="head_website + (head or '')"/>

        <div id="wrapwrap" t-att-class="pageName or ''">
            <header>
                <div class="navbar navbar-default navbar-static-top">
                    <div class="container">
                        <div class="navbar-header">
                            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-top-collapse">
                                <span class="sr-only">Toggle navigation</span>
                                <span class="icon-bar"/>
                                <span class="icon-bar"/>
                                <span class="icon-bar"/>
                            </button>
                            <a class="navbar-brand" href="/" t-if="website" t-field="website.name">My Website</a>
                        </div>
                        <div class="collapse navbar-collapse navbar-top-collapse">
                            <ul class="nav navbar-nav navbar-right" id="top_menu">
                                <t t-foreach="website.menu_id.child_id" t-as="submenu">
                                    <t t-call="website.submenu"/>
                                </t>
                                <li class="divider" t-ignore="true" t-if="website.user_id != user_id"/>
                                <li class="dropdown" t-ignore="true" t-if="website.user_id != user_id">
                                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                                        <b>
                                            <span t-esc="(len(user_id.name)&gt;25) and (user_id.name[:23]+'...') or user_id.name"/>
                                            <span class="caret"/>
                                        </b>
                                    </a>
                                    <ul class="dropdown-menu js_usermenu" role="menu">
                                        <li id="o_logout"><a t-attf-href="/web/session/logout?redirect=/" role="menuitem">Logout</a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </header>
            <main>
                <t t-raw="0"/>
            </main>
            <footer style="background: #F19122; color:#fff !important;">
                <div id="footer">
                </div>
            </footer>
        </div>
        <script id="tracking_code" t-if="website and website.google_analytics_key and not editable">
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

            ga('create', _.str.trim('<t t-esc="website.google_analytics_key"/>'), 'auto');
            ga('send','pageview');
        </script>
    </t>
</t>