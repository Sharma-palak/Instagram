from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from rest_framework import exceptions
from django.db.models import Q
from rest_framework.serializers import(ModelSerializer,EmailField)
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
'''
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self,data):
        username=data.get("username","")
        password=data.get("password","")
        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg="User is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg="Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must provide username and password both"
            raise exceptions.ValidationError(msg)

        return data

class LoginSerializer(serializers.ModelSerializer):

    username=serializers.CharField(required=False,allow_blank=True)
    email=serializers.EmailField(label='Email Address',required=False,allow_blank=True)
    class Meta:
        model=User
        fields=['username','email','password',]
        extra_kwargs={"password":{"write_only":True}
                      }
    def validate(self,data):
        user_obj = None
        email=data.get("email",None)
        username=data.get("username",None)
        password=data["password"]
        if not email and not username:
            raise ValidationError("A username or email required to login.")
        user=User.objects.filter(Q(email=email)|Q(username=username)).distinct()
        if user.exists() and user.count()==1:
            user_obj=user.first()
        else:
            raise ValidationError("This username/email is not valid. ")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password,try again")
        return data



User=get_user_model()
class UserCreateSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
        extra_kwargs={"password":{"write_only":True}
                      }

    def create(self,validated_data):
        username=validated_data['username']
        email=validated_data['email']
        #firstname=validate_data['firstname']
        #lastname=validated_data['lastname']
        password=validated_data['password']
        user_obj=User(
            username=username,
            email=email,
            #firstname=firstname,
           # lastname=lastname,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

'''
class UserSerializer1(serializers.ModelSerializer):
    email=EmailField(label='Email Address')
    email2=EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','email2', 'first_name','last_name')
        #write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {"password": {"write_only": True}}

    '''                    
    def validate_email(self,data):
        email=data['email']
        user_qs=User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This email has already been registered!!")
        return data 
    '''
    def validate_email2(self,value):
        data=self.get_initial()
        email1=data.get("email")
        email2=value
        if email1 != email2:
            raise ValidationError("Email Must Match")
        return value



    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            #email2=validated_data['email2'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user