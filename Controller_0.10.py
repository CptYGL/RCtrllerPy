# @Author : 185150736 yangganlin
#############################################
# if we wanna design a user friendly CLI interface we need to use Python to access RESTAPI , see more in 
# https://floodlight.atlassian.net/wiki/spaces/floodlightcontroller/pages/1343539/Floodlight+REST+API#FloodlightRESTAPI-FloodlightRESTAPI
# when entered the controller ip :
# access [ControllerPerformance APIs] to show status of the controller
# access [Controller APIs & Device APIs] to show info about controller , switches , devices
# main functions should include Firewall , ACL , FlowControl(static entry pusher)
# thus we should define multiple classes

#if use python3.x , the module is httplib2
#import httplib2
import httplib,json,time
#global define existing (personally prefered) request path according to RestAPI
#my PI0 runs floodlight v0.90 in default setup,some argu below shows 404 ,maybe add module?
banner = '#'*80+'\n\n'+'REMOTE CONTROLLER CLI MANIPULATOR(V0.10)\n'+'CAPABILITY : \
<AddTextHere>\n'+'NOTE : Test Eviroment ---- pi0@192.168.43.67\nNOTE : \
I also got a public ip server deployed 104.160.44.234\nNOTE : \
OTHERWISE , USE YOUR OWN INET IP ADDRESS !!!\n\n'+'#'*80
argu = {
    'ctl_con_sw':'core/controller/switches/json',                          #get
    'ctl_sum':'core/controller/summary/json',                              #get
    'ctl_mod_a':'core/module/all/json',                                        #get
    'ctl_mod_l':'core/module/loaded/json',                                  #get
    'ctl_mem':'core/memory/json',                                              #get
    'rest_status':'core/health/json',                                                #get
    'rest_ver':'core/version/json',                                                  #404,get
    'tables_mem':'core/storage/tables/json',                                  #get
    'ctl_run_time':'core/system/uptime/json',                              #get
    'ctl_role':'core/role/json',                                                     #get,post
    'sw_role':'core/switch/all/role/json',                                       #get,post
    'topo_sw_cluster':'topology/switchclusters/json',                   #get
    'topo_links':'topology/links/json',                                          #get
    'devices':'/device/',                                                                #get
    'sfep_clearall':'staticflowentrypusher/clear/all/json',              #get
    'sfep_listall':'staticflowentrypusher/list/all/json',                   #get
    'fw_status':'firewall/module/status/json',                               #get
    'fw_en':'firewall/module/enable/json',                                   #put
    'fw_dis':'firewall/module/disable/json',                                 #put
    'fw_smsk':'firewall/module/subnet-mask/json',               #get,post
    'fw_rules':'firewall/rules/json',                                             #get
    'acl_rules':'acl/rules/json',                                                     #404,get,post,delete
    'acl_clear':'acl/clear/json',                                                    #404,get
    'cperf_a':'performance/all/json',                                           #get
    'cperf_en':'performance/enable/json',                                   #post
    'cperf_dis':'performance/disable/json',                                 #post
    'cperf_rst':'performance/reset/json',                                  #post
    'cperf_dat':'performance/data/json'                                     #get
    #openflow status / multipart apis ; statistic apis ; routing apis ; Vnet filter apis not included
}
class Triggers(object):                                     #focus on GET without args
    def __init__(self,server):
        self.server = server
    def get(self,path):
        headers = { 'Content-type': 'application/json',  'Accept': 'application/json', }
        conn = httplib.HTTPConnection(self.server,8080)
        direct = '/wm/'+path
        conn.request('GET',direct,json.dumps({}),headers)
        response = conn.getresponse()
        ret = [response.status, response.reason, response.read()]
        conn.close()
        if(ret[0] == 200) : return json.loads(ret[2])
        else : return ret[1]
    def get_raw(self,opt) : 
        headers = { 'Content-type': 'application/json',  'Accept': 'application/json , text/javascript', }
        conn = httplib.HTTPConnection(self.server,8080)
        conn.request('GET','/wm/'+opt,json.dumps({}),headers)
        response = conn.getresponse()
        ret = [response.status, response.reason, response.read()]
        if(ret[0] == 200) : return ret[2]
        else : return ret[1]

class Pusher(object):                                      #this is from example python rest-api from floodlight-wiki
    def __init__(self, server):  
        self.server = server  
    def set(self,direct,data) : return self.call(direct,data, 'POST')  
    def remove(self,direct,data) : return self.call(direct,data, 'DELETE')   
    def call(self,direct, data, action):  
        headers = { 'Content-type': 'application/json',  'Accept': 'application/json', }
        path = '/wm/'+direct
        body = json.dumps(data)  
        conn = httplib.HTTPConnection(self.server, 8080,timeout=10)  
        conn.request(action, path, body, headers)  
        response = conn.getresponse()  
        ret = (response.status, response.reason, response.read())  
        conn.close()  
        if(ret[0] == 200):
            print('###From '+path+' Execute '+action+' Success!###')
            return json.loads(ret[2])
        else : return ret[1]  

def refresh(wd,t):
    print(wd)
    time.sleep(t)
print(banner)
flag = 1
try : 
    ctlip = raw_input('\nType in Controller IP (timeout 10s): ')
    trigger = Triggers(ctlip)
    while(flag):
        print('\n>>>Getting Basic Information:')
        try :
            health_status = trigger.get(argu['rest_status'])
            memory = trigger.get(argu['ctl_mem'])
            ctl_links = trigger.get(argu['ctl_sum'])
            tables = trigger.get(argu['tables_mem'])
            mod_l = trigger.get(argu['ctl_mod_l'])
            mod_a = trigger.get(argu['ctl_mod_a'])
            ctl_role = trigger.get(argu['ctl_role'])
            sw_role = trigger.get(argu['sw_role'])
            switches = trigger.get(argu['ctl_con_sw'])
            sw_cluster = trigger.get(argu['topo_sw_cluster'])
            links = trigger.get(argu['topo_links'])
            devices = trigger.get(argu['devices'])
        except Exception : 
            print('\n###Connection Failed !!! Please Rerun the Script###')
            exit(0)
        print('>>>REST Healthy ?\t\t: '+str(health_status['healthy']))
        print('>>>Module Status\t\t: '+str(len(mod_l))+' out of '+str(len(mod_a))+' Active.')
        print('>>>Current Connected\t\t: '+str(len(switches))+' Switches and '+str(len(devices))+' Devices and '+str(len(links))+' Links')
        print('>>>Current Memory Usage\t\t: '+str(memory['free'])+' / '+str(memory['total']))
        print('>>>Existed Tables\t\t: ')
        for idx in range(len(tables)) : print('table '+str(idx+1)+' : '+str(tables[idx]))
        tag = raw_input('\nWhich Option Would U Like To Choose?\n[0]Topo [1]Roles [2]FireWall [3]ACL [4]Flow [5]Route [6]CtrlPerformance [Q]QUIT\n>>>')
        if(tag=='0'):
            try:
                print('\n>>>Displaying Topology Below...')
                for ctrller in sw_cluster : 
                    print('* CTRL : '+str(ctrller)+' : ')
                    for switch in sw_cluster[ctrller] :
                        print('|------DPID(switch) : '+str(switch)+' : ')
                        for dev in devices :
                            for points in dev['attachmentPoint'] :
                                if(points['switchDPID']==switch) : 
                                    print('     |-----(PORT '+str(points['port'])+')MAC : '+str(dev['mac'])+'; IP4 : '+\
                                        str(dev['ipv4'])+'; Err_Value : '+str(points['errorStatus']))
                print('>>>Display Topology Complete !\n>>>Displaying Links Below...')
                for link in links : print('[SW '+str(link['src-switch'])+' (port '+str(link['src-port'])+' state '+str(link['src-port-state'])+')]<---'+'--->[SW '+str(link['dst-switch'])+' (port '+str(link['dst-port'])+' state '+str(link['dst-port-state'])+')]')
            except Exception: print('###Something Went Wrong!###')
            refresh('>>>Refresh in 10 seconds...',10)
        elif(tag=='1'):
            print('\nDisplaying Roles status : ')
            print('Controller Role : '+str(ctl_role['role']))
            for item in sw_role : print(str(item)+' Role : '+str(sw_role[item]['role']))
            role_flag = 1
            while(role_flag):
                change = raw_input('Now do u wanna change roles? (y/n):')
                try :
                    if(change=='y') : 
                        print('Setting Controller Role...')
                        Pusher(ctlip).set(argu['ctl_role'],{'role':str(raw_input('[ACTIVE/STANBY]: '))})
                        print('Setting Switch Role... ')
                        for item in sw_role : Pusher(ctlip).set('/core/switch/'+str(item)+'/role/json',{'role':str(raw_input(str(item)+'[MASTER/SLAVE/EQUAL]:'))})
                    elif(change=='n') : role_flag = 0
                except Exception: continue
            refresh('>>>Refresh in 5 seconds...',5)
        elif(tag=='2'):
            while(1):
                mov = raw_input('\n>>>Firewall Optionss : [info/enable/disable/mask/rule/quit] : ')
                if(mov=='info') : print('Fire Wall Enabled ? : '+str(trigger.get(argu['fw_status'])['result']))
                elif(mov=='enable') : print('Status : '+str(trigger.get(argu['fw_en'])['details']))
                elif(mov=='disable') : print('Status : '+str(trigger.get(argu['fw_dis'])['details']))
                elif(mov=='mask') : 
                    mask = trigger.get_raw(argu['fw_smsk'])
                    if(str(mask)=='') : Pusher(ctlip).set(argu['fw_smsk'],{'subnet-mask':raw_input('Your Mask : ')})
                    else : print('FW SubnetMask : '+str(mask))
                elif(mov=='rule') : #unfinished
                    print('>>>Displaying Firewall RUles:')
                    data = trigger.get(argu['fw_rules'])
                    for item in data : 
                        print(' ')
                        for k in item : print(str(k)+'\t'+str(item[k]))
                    while(1):
                        set_rule = raw_input('>>>Set new rules? (y:yes/other:quit): ')
                        if(set_rule == 'y'):
                            rule = {}
                            while(1) : 
                                key,value = raw_input('field (empty:default) : '),raw_input('value (empty:default) : ')
                                if(key == '' or value == '') : break
                                rule.update({key:value})
                            print("###Enter means all default , it's meaningless!")
                            print(rule)
                            Pusher(ctlip).set(argu['fw_rules'],rule)
                        else : break
                    while(1):
                        rm_rule = raw_input('>>>Delete rules? (y:yes/other:quit): ')
                        if(rm_rule == 'y') : Pusher(ctlip).remove(argu['fw_rules'],{'ruleid':raw_input('ruleid : ')})
                        else : break
                elif(mov=='quit') : break
                else : continue
            refresh('>>>Refresh in 5 seconds...',5)
        elif(tag=='3'):
            refresh('\n###ACL NOT SUPPORTED IN flv0.90 . UNFINISHED!!!###\n>>>Refresh in 5 seconds...',5)
        elif(tag=='4'):
            refresh('\n###FLOW NOT AVILABLE IN v0.10 . UNFINISHED!!!###\n>>>Refresh in 5 seconds...',5)
        elif(tag=='5'):
            refresh('\n###ROUTE NOT AVILABLE IN v0.10 . UNFINISHED!!!###\n>>>Refresh in 5 seconds...',5)
        elif(tag=='6'):
            ctlperf_flag = 1
            while(ctlperf_flag):
                mov = raw_input('CtrlPerf Optionss : [info/enable/disable/reset/data/quit] : ')
                if(mov=='info') : print('Controller Perf. Enabled ? : '+str(trigger.get(argu['cperf_a'])['enabled']))
                elif(mov=='enable') : print('Controller Perf. Enabled ? : '+str(trigger.get(argu['cperf_en'])['enabled']))
                elif(mov=='disable') : print('Controller Perf. Enabled ? : '+str(trigger.get(argu['cperf_dis'])['enabled']))
                elif(mov=='reset') : print('Controller Perf. Enabled ? : '+str(trigger.get(argu['cperf_rst'])['enabled']))
                elif(mov=='data') : 
                    try:
                        data = trigger.get(argu['cperf_dat'])['modules']
                        for item in data : print(str(item['module-name'])+' : Packets : '+str(item['num-packets'])+' : Average : '+str(item['average']))
                    except Exception : print('No DATA Content Available...')
                elif(mov=='quit') : break
                else : continue
            refresh('>>>Refresh in 5 seconds...',5)
        elif(tag=='Q'):
            refresh('>>>Quitting Application in 3 seconds...',3)
            flag = 0
        else : continue
except KeyboardInterrupt : 
    print('\n>>>Key Board Interrupt ! Exiting Now !\n\n:)\n')

#EOF