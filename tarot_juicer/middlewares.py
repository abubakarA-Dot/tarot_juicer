from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import AuthToggle, PassPhrase
from . import notification
from django.conf import settings

from datetime import datetime, timedelta
from django.contrib import auth, messages
from tarot_juicer.urls import urlpatterns as tarot_urls
from landings.urls import urlpatterns as landing_urls
from generators.urls import urlpatterns as generator_urls
from essays.urls import urlpatterns as essay_urls
from accounts.urls import urlpatterns as account_urls

global protected_paths
print("Ist Print")

protected_paths = [reverse('portal')]

messageSent = False

REPEATING_PATH = ""

def IS_PATH_REPEATING(request):
    global REPEATING_PATH

    if request.path != REPEATING_PATH:
        REPEATING_PATH = request.path
        return False
    else:
        return True
def ADD_PROTECTED_PATH():
    global protected_paths

    # Paths that should be protected
    protected_paths = [
        # reverse('portal'),
        tarot_urls, essay_urls,generator_urls, landing_urls, account_urls
    ]

def authentication_middleware(get_response):

    def middleware(request):
        global protected_paths, messageSent, IS_PATH_REPEATING, ADD_PROTECTED_PATH

        auth_toggle = AuthToggle.objects.first()
        faravahar = AuthToggle.objects.first()
        nuclear = AuthToggle.objects.first()
        isLoggedIn = request.user.is_authenticated
        username = request.POST.get('username')
        password = request.POST.get('password')


        # Exception if auth_toggle is not present then create one with a default value
        if auth_toggle:
            pass

        else:
            authh = AuthToggle.objects.create(is_protected = False)
            authh.save()

        # Exception if faravahar is not present then create one with a default value
        if faravahar:
            faravahar = faravahar.faravahar
        else:
            faravahar = AuthToggle.objects.create(faravahar = False)
            faravahar.save()

        # Exception if nuclear is not present then create one with a default value
        if nuclear:
            nuclear = nuclear.nuclear
        else:
            nuclear = AuthToggle.objects.create(nuclear = False)
            nuclear.save()

        admin_path = request.path.startswith(reverse('admin:index'))


        unprotected_paths = [
            reverse('index'),
        ]


        context = {
            "faravahar": faravahar,
            "nuclear": nuclear,
            "protection": AuthToggle.objects.first()
        }

        IS_LOGIN_PATH = settings.ADMIN_PATH + 'login'

        IS_LOGOUT_PATH = settings.ADMIN_PATH + 'logout'


        if IS_LOGIN_PATH in request.path and not messageSent:
            print("\n Login Path :", IS_LOGIN_PATH)
            notification.message_check_db(request)
            messageSent = True
        elif IS_LOGOUT_PATH in request.path and messageSent:
            messageSent = False

        if nuclear:
            print("\n nuclear option - Redirect to home :", nuclear)
            if isLoggedIn :
                # logic to protect paths and displaying "Admin Only Acces"
                if not admin_path:
                    if not IS_PATH_REPEATING(request):
                        print("\n admin access only message:")
                        notification.message_warn_admin_access(request)
                    else:
                        pass
                        # print("ELSE OLD MIDDLEWARE")
                        # notification.message_warn_admin_access(request)
                        # return redirect(reverse('portal'))
                else:
                    pass
            else:
                if not admin_path:
                    return render(request, 'landings/gateway.html', context)

        else:
            if username and password :
                print("\n auth toggle - Redirect to home :", auth_toggle)
                # if protection is checked and passphrase is entered then serve the portal otherwise serve gateway
                # for x in PassPhrase.objects.all().values():
                #     if request.POST.get('passphrase') == x['passphrase'] and auth_toggle.is_protected:
                #         protected_paths = []
                #         break
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    # auth.login(request, user)
                    print("\n User in middlewares middleware :", user)
                    request.session['last_touch'] = datetime.now()
                    request.session['loggedIn'] = True
                    # messages.success(request, 'You are now logged in!')
                    print("\n Logging in ===")
                    return redirect('portal')



                # if protection is checked and if logout is clicked then revert changes and serve only gateway
                if request.path.startswith(reverse('logout')) and auth_toggle.is_protected:
                    ADD_PROTECTED_PATH()
                elif not auth_toggle.is_protected:
                    protected_paths = []


                # if protection is not checked serve portal
                if not auth_toggle.is_protected and request.path in unprotected_paths and not admin_path:
                    return render(request, 'landings/portal.html', context)
                else: # else serve gateway
                    if request.path in protected_paths and not admin_path:
                        return render(request, 'landings/gateway.html', context)

        response = get_response(request)

        return response

    return middleware

def autologout_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        isLoggedIn = request.user.is_authenticated

        SESSION_TIMEOUT = AuthToggle.objects.first()
        admin_path = request.path.startswith(reverse('admin:index'))

        if not isLoggedIn:
            pass

            # try:

            #     if datetime.now() - request.session['last_touch'] > timedelta( 0, SESSION_TIMEOUT.timeout * 60, 0):

            #         ADD_PROTECTED_PATH()

            #         del request.session['last_touch']

            #         del request.session['loggedIn']

            #         notification.messages_print('error', 'Session old timeout at: ' + request.path)

            #         request.session['last_page_visited'] = request.path

            #         return redirect('/')


            #     else:
            #         notification.messages_print('success', 'Passed session validation')


            # except KeyError:
            #     pass


            if not request.session.has_key('last_touch') and request.session.has_key('loggedIn'):

                request.session['last_touch'] = datetime.now()

                notification.messages_print('info', 'New session of ' + str(SESSION_TIMEOUT.timeout) + ' minutes has started')
                print("New session started")


        else:
            notification.messages_print('warning', 'Admin access detected')

        return response

    return middleware
