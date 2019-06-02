var bytes = {}
bytes.Kb = function(x) { return Math.floor(10*x/1024)/10 }
bytes.Mb = function(x) { return Math.floor(10*x/(1024*1024))/10 }
bytes.Gb = function(x) { return Math.floor(10*x/(1024*1024*1024))/10 }
bytes.Tb = function(x) { return Math.floor(10*x/(1024*1024*1024*1024))/10 }
bytes.best = function(x) {
    if (bytes.Gb(x) > 1000) return bytes.Tb(x)+ " T"
    else if (bytes.Mb(x) > 1000) return bytes.Gb(x)+ " G"
    else if (bytes.Kb(x) > 1000) return bytes.Mb(x)+ " M"
    else if (x > 1000) return bytes.Kb(x)+ " K"
    else return x
}




